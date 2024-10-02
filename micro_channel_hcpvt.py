import numpy as np

def micro_channel_simulation(C, I, eta_ref, cof_tem, T_in, nc=12):
    # Constants
    k_cell = 138            # Thermal conductivity of cell (W/mK)
    th_cell = 0.000102      # Thickness of cell (m)
    th_fin = 0.001          # Fin thickness of inner fins (m)
    th_fino = 0.002         # Fin thickness of outer fins (m)
    y = 0.003               # Channel depth (m)
    l = y
    wm = 0.1                # Module width (m)
    z = 0.1                 # Module length (m)

    # Channel width calculation
    w = (wm - 2 * th_fino - (nc - 1) * th_fin) / nc

    # Area condition (ac)
    if w <= l:
        ac = w / l
    else:
        ac = l / w

    # Thermal properties and flow parameters
    k_di = 2.2              # Thermal conductivity of dielectric (W/mK)
    th_di = 0.000076        # Thickness of dielectric (m)
    k_cu = 401              # Thermal conductivity of copper (W/mK)
    mdot = 0.23 / nc         # Mass flow rate (kg/s)
    Dhc = (4 * y * w) / (2 * (y + w))  # Hydraulic diameter (m)
    eta_inv = 0.98          # Inverter efficiency
    eta_opt = 0.85          # Optical efficiency

    Q_inc = C * I * eta_opt # Total incident heat

    x = T_in
    on = 0
    count = 0

    while on == 0:

        if count > 0:
            x = T_w1

        # Cp calculation
        A_0 = 4.635
        A_1 = -0.3401
        B_1 = 0.5173
        A_2 = -6.857e-05
        B_2 = -0.2625
        A_3 = 0.04569
        B_3 = 0.07959
        A_4 = -0.01644
        B_4 = -0.007043
        W_0 = 0.01469
        cp = (A_0 + A_1 * np.cos(x * W_0) + B_1 * np.sin(x * W_0) + A_2 * np.cos(2 * x * W_0) +
              B_2 * np.sin(2 * x * W_0) + A_3 * np.cos(3 * x * W_0) + B_3 * np.sin(3 * x * W_0) +
              A_4 * np.cos(4 * x * W_0) + B_4 * np.sin(4 * x * W_0)) * 1000

        # u calculation
        A_00 = 38.05
        B_00 = -0.03796
        C_00 = 0.004062
        D_00 = -0.007446
        u = A_00 * np.exp(B_00 * x) + C_00 * np.exp(D_00 * x)

        # Pr calculation
        A_11, B_11, C_11 = 0.0301, 321.1, 6.813
        A_22, B_22, C_22 = -0.0533, 396.6, 70.91
        A_33, B_33, C_33 = 7.738, 262.8, 13.84
        A_44, B_44, C_44 = 0.2937, 304.6, 10.06
        A_55, B_55, C_55 = 16.71, 5345, 2736
        A_66, B_66, C_66 = 0.5821, 309.8, 26.17
        A_77, B_77, C_77 = 3.27, 280.3, 18.36
        A_88, B_88, C_88 = 1448, -537.5, 341.2

        Pr = (A_11 * np.exp(-((x - B_11) / C_11)**2) + A_22 * np.exp(-((x - B_22) / C_22)**2) +
              A_33 * np.exp(-((x - B_33) / C_33)**2) + A_44 * np.exp(-((x - B_44) / C_44)**2) +
              A_55 * np.exp(-((x - B_55) / C_55)**2) + A_66 * np.exp(-((x - B_66) / C_66)**2) +
              A_77 * np.exp(-((x - B_77) / C_77)**2) + A_88 * np.exp(-((x - B_88) / C_88)**2))

        # k calculation
        A_111, B_111, C_111 = 0.008566, 410.8, 27.14
        A_222, B_222, C_222 = 0.1057, 332, 64.75
        A_333, B_333, C_333 = 0.6727, 447.7, 235.6
        A_444, B_444, C_444 = 0.01054, 329.8, 16.47
        A_555, B_555, C_555 = 0.01993, 309.9, 15
        A_666, B_666, C_666 = 0.006941, 294, 8.932
        A_777, B_777, C_777 = 0.004508, 345.8, 2.7
        A_888, B_888, C_888 = 0.1425, 264.4, 37.66

        k = (A_111 * np.exp(-((x - B_111) / C_111)**2) + A_222 * np.exp(-((x - B_222) / C_222)**2) +
             A_333 * np.exp(-((x - B_333) / C_333)**2) + A_444 * np.exp(-((x - B_444) / C_444)**2) +
             A_555 * np.exp(-((x - B_555) / C_555)**2) + A_666 * np.exp(-((x - B_666) / C_666)**2) +
             A_777 * np.exp(-((x - B_777) / C_777)**2) + A_888 * np.exp(-((x - B_888) / C_888)**2))

        # Heat and Reynolds calculations
        Q_a = 2 * mdot * cp * T_in
        Re = (mdot * Dhc) / (y * w * u)

        # Friction factor F
        if Re <= 20000:
            F = 0.316 * (Re ** -0.25)
        else:
            F = 0.184 * (Re ** -0.2)

        # Nusselt number Nu
        if Re <= 2300:
            Nu = 8.235 * (1 - 2.0421 * ac + 3.0853 * ac**2 - 2.476 * ac**3 + 1.0578 * ac**4 - 0.1861 * ac**5)
        else:
            Nu = ((F / 8) * (Re - 1000) * Pr) / (l + (12.7 * (F / 8)**0.5) * (Pr**0.667 - l))

        # Heat transfer coefficient h
        h = (Nu * k) / Dhc

        # Matrix coefficients
        a1 = (k_cell / th_cell)
        a2 = a1
        a3 = -(k_cell / th_cell) - (k_di / th_di)
        a4 = (k_di / th_di)
        a5 = a4 * w * z
        a6 = -h * z * w + 2 * h * z * th_fin - a5 - 2 * k_cu * th_fin * (z / l)
        a7 = 2 * k_cu * th_fin * (z / l)
        a8 = -2 * h * z * th_fin + h * z * w
        a9 = 2 * k_cu * th_fin * (z / l) - 0.5 * h * z * l
        a10 = -2 * k_cu * th_fin * (z / l) - 0.5 * h * z * l
        a11 = h * z * l
        a12 = h * z * w + 0.5 * h * z * l - 2 * h * z * th_fin
        a13 = 0.5 * h * z * l
        a14 = -2 * mdot * cp - h * z * w - h * z * l + 2 * h * z * th_fin

        # Matrix A and vector B
        if count > 0:
            T_w2 = X[4]

        A = [[a1 + cof_tem * Q_inc, -a1, 0, 0, 0],
             [a2, a3, a4, 0, 0],
             [0, a5, a6, a7, a8],
             [0, 0, a9, a10, a11],
             [0, 0, a12, a13, a14]]

        B = [(1 - eta_ref + cof_tem * 298) * Q_inc, 0, 0, 0, -Q_a]

        # Solve the system of equations
        X = np.linalg.solve(A, B)
        T_cell = X[0]
        T_w1 = X[4]

        if count > 0:
            if abs(T_w1 - T_w2) < 0.001:
                on = 1

        count += 1

    # Calculate T_cell, T_w1, and T_out
    T_cell_Celsius = T_cell - 273  # Convert T_cell to Celsius
    T_w1_Celsius = T_w1  # T_w1 as it is
    T_out = 2 * X[4] - T_in  # Assuming X[5] corresponds to the fifth element (index 4 in Python)

    # Efficiency calculations
    eta_pv = eta_ref - (cof_tem * (T_cell - 298))  # PV efficiency
    eta_el = eta_pv * eta_inv  # Electrical efficiency
    eta_th = (nc * mdot * cp * (T_out - T_in)) / (eta_opt * C * I * wm * z)  # Thermal efficiency

    # Power calculations
    P_el = C * I * wm * z * eta_el  # Electrical power
    P_th = C * I * wm * z * eta_th  # Thermal power

    # Pressure drop calculation (delta_p)
    delta_p = F * z * 1050 * ((mdot / (1050 * w * l))**2) / (2 * Dhc)

    # Return the results
    return {
        'T_cell_Celsius': T_cell_Celsius,
        'T_w1_Celsius': T_w1_Celsius,
        'T_out': T_out,
        'eta_pv': eta_pv,
        'eta_el': eta_el,
        'eta_th': eta_th,
        'P_el': P_el,
        'P_th': P_th,
        'delta_p': delta_p
    }

# Example usage
results = micro_channel_simulation(C=1100, I=1000, eta_ref=0.322, cof_tem=0.0007, T_in=357)
print(results)