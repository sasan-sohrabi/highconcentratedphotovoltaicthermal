def simulate_system(C, I, eta_ref, cof_tem, T_in_hcpvt, nc=12, previous_tank_temp=50, previous_water_storage=100,
                    previous_hydrogen_storage=100, max_water_storage=500, max_hydrogen_storage=1000, hour_of_day=12,
                    solar_irradiance_pv=1000):
    """
    Full system simulation for one hour, integrating HCPVT, PV panels, on-grid electricity, pipeline water, and fuel cell.
    """
    # Step 1: Simulate HCPVT unit
    hcpvt_results = hcpvt_simulation(C, I, eta_ref, cof_tem, T_in_hcpvt, nc)

    # Step 2: Simulate PV panels to supplement electricity
    electricity_pv = pv_panels_simulation(solar_irradiance_pv)

    # Total electricity available from HCPVT and PV
    electricity_available = hcpvt_results['P_el'] + electricity_pv

    # Step 3: Simulate MED desalination to produce fresh water
    water_produced, T_out_desalination = med_desalination(hcpvt_results['P_th'], hcpvt_results['T_out'])

    # Step 4: Simulate water tank management
    water_storage, water_deficit = water_tank_management(water_produced, 0, previous_water_storage, max_water_storage)

    # If there is a water deficit, use pipeline water
    if water_deficit > 0:
        pipeline_water_used = water_deficit
        water_storage += pipeline_water_used
    else:
        pipeline_water_used = 0

    # Step 5: Simulate electrolyzer using the available electricity and water
    hydrogen_produced, water_consumed, T_out_electrolyzer = electrolyzer(electricity_available, T_out_desalination)

    # Step 6: Update hydrogen storage based on production and consumption
    hydrogen_demand = hydrogen_demand_profile(hour_of_day)
    hydrogen_storage, hydrogen_excess = hydrogen_storage_management(hydrogen_produced, hydrogen_demand,
                                                                    previous_hydrogen_storage, max_hydrogen_storage)
