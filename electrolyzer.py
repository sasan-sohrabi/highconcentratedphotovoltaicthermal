def electrolyzer_simulation_calculate_requirements(hydrogen_demand, efficiency_ez=0.75, LHV=33.33, water_needed_per_kg_h2=9, X_ST=0.9):
    """
    Simulate the electrolyzer to calculate electricity and water needed to meet the hydrogen demand.
    :param hydrogen_demand: The hydrogen demand for the current hour (kg).
    :param efficiency_ez: Efficiency of the electrolyzer (fraction between 0 and 1).
    :param LHV: Lower Heating Value of hydrogen (kWh/kg).
    :param water_needed_per_kg_h2: Amount of water needed to produce 1 kg of hydrogen (kg).
    :param X_ST: Water utilization factor (the efficiency with which water is converted into hydrogen).
    :return: A dictionary with electricity needed, water needed, and hydrogen produced.
    """

    # Calculate how much electricity is needed to produce the hydrogen demand
    electricity_needed_per_kg_h2 = LHV / efficiency_ez
    total_electricity_needed = hydrogen_demand * electricity_needed_per_kg_h2

    # Calculate how much water is needed to produce the hydrogen demand
    total_water_needed = hydrogen_demand * water_needed_per_kg_h2

    # Calculate the blowdown water (water returned to the system)
    blowdown_water = total_water_needed * (1 - X_ST)

    return {
        'hydrogen_produced': hydrogen_demand,
        'electricity_needed': total_electricity_needed,
        'water_needed': total_water_needed,
        'blowdown_water': blowdown_water
    }

# Example usage of the electrolyzer simulation
hydrogen_demand = 50  # kg (hydrogen demand for the current hour)
electrolyzer_results = electrolyzer_simulation_calculate_requirements(hydrogen_demand)

# Output results
print(f"Hydrogen produced: {electrolyzer_results['hydrogen_produced']:.2f} kg")
print(f"Electricity needed: {electrolyzer_results['electricity_needed']:.2f} kWh")
print(f"Water needed: {electrolyzer_results['water_needed']:.2f} kg")
print(f"Blowdown water: {electrolyzer_results['blowdown_water']:.2f} kg")