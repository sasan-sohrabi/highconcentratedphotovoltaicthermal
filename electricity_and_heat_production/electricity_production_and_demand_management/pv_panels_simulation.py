def pv_panels_simulation(irradiance, ambient_temp, wind_speed, rated_power_pv=500, gamma_pv_p=-0.35,
                         irradiance_stc=1000, theta_stc=25, theta_noct=45, ambient_noct=20,
                         irradiance_noct=800, k=0.05):
    """
    Simulate the power output of the PV panels based on irradiance, temperature, and wind speed.
    :param irradiance: The irradiance at the current time (W/m²).
    :param ambient_temp: The ambient temperature at the current time (°C).
    :param rated_power_pv: The rated power output of the PV panels (kW).
    :param gamma_pv_p: The temperature coefficient for the PV panels (%/°C).
    :param wind_speed: The wind speed at the current time (m/s).
    :param irradiance_stc: The irradiance at standard test conditions (W/m²).
    :param theta_stc: The cell temperature at standard test conditions (°C).
    :param theta_noct: The cell temperature at nominal operating conditions (°C).
    :param ambient_noct: The ambient temperature at nominal operating conditions (°C).
    :param irradiance_noct: The irradiance at nominal operating conditions (W/m²).
    :param k: Wind cooling coefficient (default is 0.05).
    :return: Power output of the PV system (kW).
    """

    # Step 1: Calculate the cell temperature based on ambient temperature, irradiance, and wind speed
    cell_temp = ambient_temp + ((theta_noct - ambient_noct) / irradiance_noct) * irradiance * (1 / (1 + k * wind_speed))

    # Step 2: Calculate the temperature-adjusted power output
    power_output = rated_power_pv * (irradiance / irradiance_stc) * (1 + (gamma_pv_p / 100) * (cell_temp - theta_stc))

    return power_output


"""
# Example usage of the PV simulation with wind effect
irradiance = 1000  # W/m² (current irradiance)
ambient_temp = 25  # °C (current ambient temperature)
wind_speed = 10  # m/s (current wind speed)

# Simulate the PV panel power output with wind effect
pv_power_output = pv_panels_simulation(irradiance, ambient_temp, wind_speed)

# Output result
print(f"PV power output with wind effect: {pv_power_output:.2f} kW")
"""
