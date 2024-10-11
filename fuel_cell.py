def fuel_cell_simulation(hydrogen_available, efficiency_fc=0.55, LHV=33.33, MW=18.015, MH=2.016, DW=1000):
    """
    Simulate the fuel cell's electricity production and water production based on the hydrogen input.
    :param hydrogen_available: Amount of hydrogen available for the fuel cell (kg).
    :param efficiency_fc: Efficiency of the fuel cell (fraction between 0 and 1).
    :param LHV: Lower Heating Value of hydrogen (kWh/kg).
    :param MW: Molar mass of water (g/mol).
    :param MH: Molar mass of hydrogen (g/mol).
    :param DW: Density of water (kg/m^3).
    :return: Electricity produced (kWh), water produced (kg).
    """

    # Calculate the electricity produced by the fuel cell
    electricity_produced = hydrogen_available * efficiency_fc * LHV

    # Calculate the water produced by the fuel cell
    # Water production is based on the reaction of hydrogen and oxygen
    water_produced = hydrogen_available * (MW / (MH * DW))

    # Return the results
    return {
        'electricity_produced': electricity_produced,
        'water_produced': water_produced
    }


# Example usage of the fuel cell simulation
hydrogen_available = 10  # kg of hydrogen available for the fuel cell
fuel_cell_results = fuel_cell_simulation(hydrogen_available)

# Output results
print(f"Electricity produced: {fuel_cell_results['electricity_produced']:.2f} kWh")
print(f"Water produced: {fuel_cell_results['water_produced']:.4f} kg")
