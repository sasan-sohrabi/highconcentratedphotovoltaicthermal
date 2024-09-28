import numpy as np

def micro22(C, I, eta_ref, cof_tem, T_in, nc):
    # Material and geometric properties
    k_cell, th_cell = 138, 0.000102   # Cell thermal conductivity (W/mK) and thickness (m)
    th_fin, th_fino = 0.001, 0.002    # Inner and outer fin thicknesses (m)
    y, wm, z = 0.003, 0.1, 0.1        # Channel depth, module width, and length (m)
    w = (wm - 2 * th_fino - (nc - 1) * th_fin) / nc  # Channel width

    ac = w / y if w <= y else y / w   # Aspect ratio of the channel
    k_di, th_di = 2.2, 0.000076       # Dielectric properties
    k_cu = 401                        # Copper thermal conductivity (W/mK)
    mdot = 0.2 / nc                   # Mass flow rate (kg/s)
    Dhc = (4 * y * w) / (2 * (y + w)) # Hydraulic diameter (m)
    eta_inv, eta_opt = 0.98, 0.85     # Inverter and optical efficiencies
    Q_inc = C * I * eta_opt           # Total incident heat

    # Initialize variables
    x, on, count = T_in, 0, 0

    while on == 0:
        if count > 0:
            x = T_w1

        # Specific heat (cp) calculation
        W_0 = 0.01469
        A_coeff = [4.635, -0.3401, 0.04569, -0.01644]
        B_coeff = [0.5173, -0.2625, 0.07959, -0.007043]
        cp = sum(A * np.cos(i * x * W_0) + B * np.sin(i * x * W_0)
                 for i, (A, B) in enumerate(zip(A_coeff, B_coeff), 1)) * 1000

        # Dynamic viscosity (u) calculation
        A_00, B_00, C_00, D_00 = 38.05, -0.03796, 0.004062, -0.007446
        u = A_00 * np.exp(B_00 * x) + C_00 * np.exp(D_00 * x)

        # Prandtl number (Pr) calculation
        A_params = [0.0301, -0.0533, 7.738, 0.2937]
        B_params = [321.1, 396.6, 262.8, 304.6]
        C_params = [6.813, 70.91, 13.84, 10.06]
        Pr = sum(A * np.exp(-((x - B) / C)**2)
                 for A, B, C in zip(A_params, B_params, C_params))

        # Heat transfer calculations
        Q_a = 2 * mdot * cp * T_in
        Re = (mdot * Dhc) / (y * w * u)

        # Friction factor (F) and Nusselt number (Nu)
        F = 0.316 * Re**-0.25 if Re <= 20000 else 0.184 * Re**-0.2
        if Re <= 2300:
            Nu = 8.235 * (1 - 2.0421 * ac + 3.0853 * ac**2 - 2.476 * ac**3 + 1.0578 * ac**4 - 0.1861 * ac**5)
        else:
            Nu = ((F / 8) * (Re - 1000) * Pr) / (1 + (12.7 * (F / 8)**0.5) * (Pr**0.667 - 1))

        h = (Nu * Pr) / Dhc

        # System of equations to calculate temperature
        a1 = k_cell / th_cell
        a3 = -(k_cell / th_cell) - (k_di / th_di)
        a4 = k_di / th_di
        a5 = a4 * w * z
        a6 = -h * z * w + 2 * h * z * th_fin - a5 - 2 * k_cu * th_fin * (z / y)
        a7 = 2 * k_cu * th_fin * (z / y)
        a8 = -2 * h * z * th_fin + h * z * w
        a9 = 2 * k_cu * th_fin * (z / y) - 0.5 * h * z * y
        a10 = -2 * k_cu * th_fin * (z / y) - 0.5 * h * z * y
        a11 = h * z * y

        # Matrix A and B
        A = np.array([
            [a1 + cof_tem * Q_inc, -a1, 0, 0, 0],
            [a1, a3, a4, 0, 0],
            [0, a5, a6, a7, a8],
            [0, 0, a9, a10, a11],
            [0, 0, 0, h * z * y + 0.5 * h * z * y - 2 * h * z * th_fin,
             -2 * mdot * cp - h * z * w - h * z * y + 2 * h * z * th_fin]
        ])
        B = np.array([(1 - eta_ref + cof_tem * 298) * Q_inc, 0, 0, 0, -Q_a])

        # Solve the system of equations
        X = np.linalg.solve(A, B)
        T_cell, T_w1 = X[0], X[4]

        if count > 0 and abs(T_w1 - T_w2) < 0.001:
            on = 1

        T_w2 = T_w1
        count += 1

    T_out = 2 * T_w1 - T_in  # Outlet temperature
    eta_pv = eta_ref - (cof_tem * (T_cell - 298))
    eta_el = eta_pv * eta_inv
    eta_th = (nc * mdot * cp * (T_out - T_in)) / (eta_opt * C * I * wm * z)
    P_el = C * I * wm * z * eta_el
    P_th = C * I * wm * z * eta_th
    delta_p = F * z * 1050 * ((mdot / (1050 * w * y))**2) / (2 * Dhc)

    return T_cell - 273, T_w1, T_out, eta_pv, eta_el, eta_th, P_el, P_th, delta_p

micro22(1000, 1000, 0.322, 0.0007, 357.3, 12)