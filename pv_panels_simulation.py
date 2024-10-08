def pv_panels_simulation(irradiance, ambient_temp, rated_power_pv, gamma_pv_p, irradiance_stc=1000, theta_stc=25, theta_noct=45, ambient_noct=20, irradiance_noct=800):
    """
    Simulate the power output of the PV panels based on irradiance and temperature.
    :param irradiance: The irradiance at the current time (W/m²).
    :param ambient_temp: The ambient temperature at the current time (°C).
    :param rated_power_pv: The rated power output of the PV panels (kW).
    :param gamma_pv_p: The temperature coefficient for the PV panels (%/°C).
    :param irradiance_stc: The irradiance at standard test conditions (W/m²).
    :param theta_stc: The cell temperature at standard test conditions (°C).
    :param theta_noct: The cell temperature at nominal operating conditions (°C).
    :param ambient_noct: The ambient temperature at nominal operating conditions (°C).
    :param irradiance_noct: The irradiance at nominal operating conditions (W/m²).
    :return: Power output of the PV system (kW).
    """

    # Step 1: Calculate the cell temperature based on ambient temperature and irradiance
    cell_temp = ambient_temp + ((theta_noct - ambient_noct) / irradiance_noct) * irradiance

    # Step 2: Calculate the temperature-adjusted power output
    power_output = rated_power_pv * (irradiance / irradiance_stc) * (1 + (gamma_pv_p / 100) * (cell_temp - theta_stc))

    return power_output

# Example usage of the PV simulation
irradiance = 1000  # W/m² (current irradiance)
ambient_temp = 20  # °C (current ambient temperature)
rated_power_pv = 10  # kW (rated power of PV system)
gamma_pv_p = -0.5  # %/°C (temperature coefficient of PV panels)

# Simulate the PV panel power output
pv_power_output = pv_panels_simulation(irradiance, ambient_temp, rated_power_pv, gamma_pv_p)

# Output result
print(f"PV power output: {pv_power_output:.2f} kW")
