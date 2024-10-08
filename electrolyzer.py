def electrolyzer_simulation(electricity_available, water_available, water_needed_per_kg_h2=9,
                            electricity_needed_per_kg_h2=50, blowdown_fraction=0.1):
    """
    Simulate the electrolyzer's hydrogen production, water consumption, and electricity usage.
    :param electricity_available: Total electricity available for the electrolyzer (kWh).
    :param water_available: Total water available for the electrolyzer (kg).
    :param water_needed_per_kg_h2: Amount of water needed to produce 1 kg of hydrogen (kg).
    :param electricity_needed_per_kg_h2: Amount of electricity needed to produce 1 kg of hydrogen (kWh).
    :param blowdown_fraction: Fraction of water returned as blowdown.
    :return: Hydrogen produced (kg), water consumed (kg), blowdown water (kg), electricity used (kWh).
    """

    # Maximum hydrogen production limited by either electricity or water
    max_h2_from_electricity = electricity_available / electricity_needed_per_kg_h2  # kg of hydrogen producible
    max_h2_from_water = water_available / water_needed_per_kg_h2  # kg of hydrogen producible

    # Hydrogen production is limited by the smaller of the two
    hydrogen_produced = min(max_h2_from_electricity, max_h2_from_water)

    # Calculate the water and electricity consumption based on hydrogen production
    water_consumed = hydrogen_produced * water_needed_per_kg_h2
    electricity_used = hydrogen_produced * electricity_needed_per_kg_h2

    # Calculate blowdown water (water returned to the system)
    blowdown_water = water_consumed * blowdown_fraction

    # Return the results
    return {
        'hydrogen_produced': hydrogen_produced,
        'water_consumed': water_consumed,
        'blowdown_water': blowdown_water,
        'electricity_used': electricity_used
    }


# Example usage of the electrolyzer simulation
electricity_available = 1000  # kWh
water_available = 500  # kg

electrolyzer_results = electrolyzer_simulation(electricity_available, water_available)

# Output results
print(f"Hydrogen produced: {electrolyzer_results['hydrogen_produced']:.2f} kg")
print(f"Water consumed: {electrolyzer_results['water_consumed']:.2f} kg")
print(f"Blowdown water: {electrolyzer_results['blowdown_water']:.2f} kg")
print(f"Electricity used: {electrolyzer_results['electricity_used']:.2f} kWh")
