def fuel_cell(hydrogen_excess, fuel_cell_efficiency=0.6, kwh_per_kg_hydrogen=50):
    """
    Simulate fuel cell electricity production using excess hydrogen.
    :param hydrogen_excess: Excess hydrogen available (kg).
    :param fuel_cell_efficiency: Efficiency of the fuel cell.
    :return: Electricity generated for export (kWh).
    """
    electricity_exported = hydrogen_excess * fuel_cell_efficiency * kwh_per_kg_hydrogen
    return electricity_exported
