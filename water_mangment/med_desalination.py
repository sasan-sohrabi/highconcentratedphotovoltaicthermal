def med_desalination(P_th, T_in, efficiency=0.85, heat_kwh_per_kg_water=0.1):
    """
    Simulate MED desalination and track water production and outlet temperature.
    :param P_th: Thermal power available (kWh).
    :param T_in: Inlet water temperature (°C).
    :return: Water produced (kg) and outlet water temperature (°C).
    """
    # Water production calculation
    water_produced = (P_th * efficiency) / heat_kwh_per_kg_water
    T_out = T_in - 10  # Assume the temperature drops by 10°C during desalination
    return water_produced, T_out
