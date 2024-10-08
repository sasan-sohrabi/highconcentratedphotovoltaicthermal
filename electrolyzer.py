def electrolyzer(electricity_available, T_in, efficiency=0.75, kwh_per_kg_hydrogen=50, water_per_kg_hydrogen=9):
    """
    Simulate hydrogen production in the electrolyzer and track water consumption.
    :param electricity_available: Total electricity available (kWh).
    :param T_in: Inlet water temperature (°C).
    :param water_per_kg_hydrogen: Water consumed per kg of hydrogen produced (kg water/kg hydrogen).
    :return: Hydrogen produced (kg), water consumed (kg), and outlet water temperature (°C).
    """
    hydrogen_produced = (electricity_available * efficiency) / kwh_per_kg_hydrogen
    water_consumed = hydrogen_produced * water_per_kg_hydrogen
    T_out = T_in + 5  # Assume temperature increases by 5°C due to electrolysis
    return hydrogen_produced, water_consumed, T_out
