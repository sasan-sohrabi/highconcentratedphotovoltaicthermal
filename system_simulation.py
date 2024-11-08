
from water_mangment.electrolyzer import electrolyzer
from electricity_and_heat_production.electricity_production_and_demand_management.fuel_cell_simulation import fuel_cell
from electricity_and_heat_production.cogenration_and_heat_production.hcpvt_simulation import hcpvt_simulation
from hydrogen_demand_calculation.hourly_hydrogen_demand_fuel_staion import hydrogen_demand_profile_8760
from hydrogen_production.hydrogen_storage_management import hydrogen_storage_management
from water_mangment.med_desalination import med_desalination
from electricity_and_heat_production.electricity_production_and_demand_management.on_grid_electricity_management import on_grid_electricity_management
from electricity_and_heat_production.electricity_production_and_demand_management.pv_panels_simulation import pv_panels_simulation
from water_mangment.water_tank_management import water_tank_management


def simulate_system_for_year(C, I, eta_ref, cof_tem, T_in_hcpvt, nc=12, max_water_storage=500,
                             max_hydrogen_storage=1000, solar_irradiance_pv=1000):
    """
    Simulate the system for 8760 hours (1 year) based on hydrogen demand and system behavior.
    """
    # Initialize storage values and lists to track the results
    previous_tank_temp = 50  # Initial water temperature (°C)
    previous_water_storage = 100  # Initial water storage (kg)
    previous_hydrogen_storage = 100  # Initial hydrogen storage (kg)

    results = {
        'hourly_hydrogen_produced': [],
        'hourly_hydrogen_used': [],
        'hourly_water_produced': [],
        'hourly_water_consumed': [],
        'hourly_electricity_deficit': [],
        'hourly_electricity_exported': [],
        'hourly_pipeline_water_used': [],
        'hourly_hydrogen_storage': []
    }

    # Get the hydrogen demand for 8760 hours
    hourly_hydrogen_demand = hydrogen_demand_profile_8760()

    # Simulate for each of the 8760 hours
    for hour in range(8760):
        hour_of_day = hour % 24  # Get the hour of the day (0-23)

        # Step 1: Simulate HCPVT unit for this hour
        hcpvt_results = hcpvt_simulation(C, I, eta_ref, cof_tem, T_in_hcpvt, nc)

        # Step 2: Simulate PV panels for this hour
        electricity_pv = pv_panels_simulation(solar_irradiance_pv)

        # Total electricity available
        electricity_available = hcpvt_results['P_el'] + electricity_pv

        # Step 3: Simulate MED desalination for water production
        water_produced, T_out_desalination = med_desalination(hcpvt_results['P_th'], hcpvt_results['T_out'])

        # Step 4: Simulate water tank management
        water_storage, water_deficit = water_tank_management(water_produced, 0, previous_water_storage,
                                                             max_water_storage)

        # If there's a water deficit, use pipeline water
        if water_deficit > 0:
            pipeline_water_used = water_deficit
            water_storage += pipeline_water_used
        else:
            pipeline_water_used = 0

        # Step 5: Simulate electrolyzer
        hydrogen_produced, water_consumed, T_out_electrolyzer = electrolyzer(electricity_available, T_out_desalination)

        # Step 6: Simulate hydrogen storage and consumption
        hydrogen_demand = hourly_hydrogen_demand[hour]
        hydrogen_storage, hydrogen_excess = hydrogen_storage_management(hydrogen_produced, hydrogen_demand,
                                                                        previous_hydrogen_storage, max_hydrogen_storage)

        # Step 7: Simulate fuel cell for grid export if there is excess hydrogen
        if hydrogen_excess > 0:
            electricity_exported = fuel_cell(hydrogen_excess)
        else:
            electricity_exported = 0

        # Step 8: On-grid electricity management if there's electricity deficit
        electricity_needed = hydrogen_produced * 50  # Assume 50 kWh per kg of hydrogen
        on_grid_electricity, electricity_deficit = on_grid_electricity_management(electricity_needed,
                                                                                  electricity_available)

        # Store the results of the current hour
        results['hourly_hydrogen_produced'].append(hydrogen_produced)
        results['hourly_hydrogen_used'].append(hydrogen_demand)
        results['hourly_water_produced'].append(water_produced)
        results['hourly_water_consumed'].append(water_consumed)
        results['hourly_electricity_deficit'].append(electricity_deficit)
        results['hourly_electricity_exported'].append(electricity_exported)
        results['hourly_pipeline_water_used'].append(pipeline_water_used)
        results['hourly_hydrogen_storage'].append(hydrogen_storage)

        # Update previous storage values for the next hour
        previous_water_storage = water_storage
        previous_hydrogen_storage = hydrogen_storage

    return results


# Example usage for the simulation
C = 1100
I = 1000
eta_ref = 0.322
cof_tem = 0.0007
T_in_hcpvt = 357  # Inlet temperature to the HCPVT system in Kelvin
solar_irradiance_pv = 1000  # Solar irradiance for PV panels in W/m^2

# Simulate for the entire year (8760 hours)
results = simulate_system_for_year(C, I, eta_ref, cof_tem, T_in_hcpvt, nc=12, max_water_storage=500,
                                   max_hydrogen_storage=1000, solar_irradiance_pv=solar_irradiance_pv)

# Example summary of the results
total_hydrogen_produced = sum(results['hourly_hydrogen_produced'])
total_hydrogen_demand = sum(results['hourly_hydrogen_used'])
total_electricity_exported = sum(results['hourly_electricity_exported'])
total_electricity_deficit = sum(results['hourly_electricity_deficit'])
total_pipeline_water_used = sum(results['hourly_pipeline_water_used'])

print(f"Total hydrogen produced in a year: {total_hydrogen_produced:.2f} kg")
print(f"Total hydrogen demand in a year: {total_hydrogen_demand:.2f} kg")
print(f"Total electricity exported to the grid: {total_electricity_exported:.2f} kWh")
print(f"Total electricity deficit (on-grid usage): {total_electricity_deficit:.2f} kWh")
print(f"Total pipeline water used: {total_pipeline_water_used:.2f} kg")
