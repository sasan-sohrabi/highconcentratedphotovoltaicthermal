def pv_panels_simulation(solar_irradiance, panel_efficiency=0.18, panel_area=100):
    """
    Simulate PV panel electricity production.
    :param solar_irradiance: Solar irradiance (W/m^2).
    :param panel_efficiency: Efficiency of the PV panels.
    :param panel_area: Total area of the PV panels (m^2).
    :return: Electricity produced by the PV panels (kWh).
    """
    electricity_pv = solar_irradiance * panel_efficiency * panel_area / 1000  # Convert W to kWh
    return electricity_pv