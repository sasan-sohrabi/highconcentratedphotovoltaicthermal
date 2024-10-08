def on_grid_electricity_management(electricity_needed, electricity_available):
    """
    Calculate on-grid electricity if the system's electricity is insufficient.
    :param electricity_needed: Total electricity needed (kWh).
    :param electricity_available: Electricity available from HCPVT and PV panels (kWh).
    :return: On-grid electricity used (kWh), electricity deficit (kWh).
    """
    if electricity_available >= electricity_needed:
        return 0, 0  # No grid electricity needed
    else:
        return electricity_needed - electricity_available, electricity_needed - electricity_available
