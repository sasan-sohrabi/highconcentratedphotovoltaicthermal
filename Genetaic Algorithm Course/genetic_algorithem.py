import numpy as np
from deap import base, creator, tools, algorithms

# Define multi-objective fitness (Minimize cost, Maximize exergy)
creator.create("FitnessMulti", base.Fitness, weights=(-1.0, 1.0))  # Minimize cost, maximize exergy
creator.create("Individual", list, fitness=creator.FitnessMulti)


# Step 2: Define individual (system configuration)
def create_individual():
    hcpvt_size = np.random.randint(1, 20)  # HCPVT size in units (integer)
    pv_size = np.random.uniform(50, 500)  # PV size in kW
    hydrogen_tank_size = np.random.uniform(1000, 10000)  # Hydrogen tank in kg
    auxiliary_heater_size = np.random.uniform(0.5, 5.0)  # Auxiliary heater in MW
    grid_usage = np.random.uniform(0.0, 1.0)  # Grid usage factor (0 to 1)
    adsorption_chiller_size = np.random.uniform(0.1, 2.0)  # Adsorption chiller in MW

    return [hcpvt_size, pv_size, hydrogen_tank_size, auxiliary_heater_size, grid_usage, adsorption_chiller_size]


toolbox = base.Toolbox()
toolbox.register("individual", tools.initIterate, creator.Individual, create_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Step 3: Define system efficiencies and constants
electrolyzer_efficiency = 50  # 50 kWh produces 1 kg of hydrogen
fuel_cell_efficiency = 0.5  # 50% efficiency in converting hydrogen to electricity

# Define hourly demand arrays (8760 hours for one year)
hydrogen_demand = np.random.uniform(10, 100, 8760)  # Hydrogen demand in kg (replace with real data)
heat_demand = np.random.uniform(20, 200, 8760)  # Heat demand in kW (replace with real data)
cooling_demand = np.random.uniform(15, 150, 8760)  # Cooling demand in kW (replace with real data)


# Step 4: Fitness function with electrolyzer, fuel cell, and hydrogen storage
def evaluate(individual):
    hcpvt_size, pv_size, hydrogen_tank_size, auxiliary_heater_size, grid_usage, adsorption_chiller_size = individual

    # HCPVT electricity and heat production
    electricity_hcpvt_per_unit = 2.5  # kW per HCPVT unit
    heat_hcpvt_per_unit = 5.5  # kW per HCPVT unit

    # Calculate total electricity and heat from HCPVT based on number of units
    total_electricity_hcpvt = hcpvt_size * electricity_hcpvt_per_unit  # Total electricity from HCPVT
    total_heat_hcpvt = hcpvt_size * heat_hcpvt_per_unit  # Total heat from HCPVT

    # Initialize hydrogen tank storage
    hydrogen_storage = 0  # kg of hydrogen in the tank

    # Initialize total cost and exergy efficiency calculations
    total_cost = 0
    unmet_hydrogen_demand = 0
    unmet_heat_demand = 0
    unmet_cooling_demand = 0
    total_exergy_efficiency = 0

    for hour in range(8760):
        # Hourly demands (replace with real data)
        hydrogen_demand_hour = hydrogen_demand[hour]
        heat_demand_hour = heat_demand[hour]
        cooling_demand_hour = cooling_demand[hour]

        # Simulate PV and grid electricity production
        electricity_pv = pv_size * np.random.uniform(0.2, 0.9)  # Simulate PV electricity
        electricity_grid = grid_usage * np.random.uniform(0.0, 1.0) * 100  # Simulate grid electricity

        # Total electricity available for electrolysis (HCPVT + PV + grid)
        total_electricity = total_electricity_hcpvt + electricity_pv + electricity_grid

        # Electrolysis to produce hydrogen (50 kWh produces 1 kg of hydrogen)
        hydrogen_produced = total_electricity / electrolyzer_efficiency

        # Store excess hydrogen in the tank
        hydrogen_storage += hydrogen_produced

        # Check if hydrogen demand is met
        if hydrogen_storage >= hydrogen_demand_hour:
            # Hydrogen demand is met, deduct from storage
            hydrogen_storage -= hydrogen_demand_hour
        else:
            # If not enough hydrogen, the deficit is recorded
            unmet_hydrogen_demand += (hydrogen_demand_hour - hydrogen_storage)
            hydrogen_storage = 0  # Tank is empty

        # If electricity demand is unmet, use hydrogen in the fuel cell
        if total_electricity < hydrogen_demand_hour:
            hydrogen_needed_for_fuel_cell = (hydrogen_demand_hour - total_electricity) * fuel_cell_efficiency
            if hydrogen_storage >= hydrogen_needed_for_fuel_cell:
                # Use hydrogen in fuel cell to produce electricity
                total_electricity += hydrogen_needed_for_fuel_cell / fuel_cell_efficiency
                hydrogen_storage -= hydrogen_needed_for_fuel_cell
            else:
                # Not enough hydrogen to meet electricity demand
                unmet_hydrogen_demand += (hydrogen_needed_for_fuel_cell - hydrogen_storage)
                hydrogen_storage = 0  # Tank is empty

        # Heat production (HCPVT + auxiliary heater)
        heat_aux = auxiliary_heater_size * np.random.uniform(0.5, 1.0)  # Auxiliary heater heat production
        total_heat = total_heat_hcpvt + heat_aux

        # Cooling production (adsorption chiller)
        cooling_produced = adsorption_chiller_size * np.random.uniform(0.6, 1.0)  # Cooling

        # Check unmet heat and cooling demands
        if total_heat < heat_demand_hour:
            unmet_heat_demand += (heat_demand_hour - total_heat)
        if cooling_produced < cooling_demand_hour:
            unmet_cooling_demand += (cooling_demand_hour - cooling_produced)

        # Add costs (grid and auxiliary heater)
        cost_grid = grid_usage * 0.1 * 100  # Simplified grid cost per hour
        cost_aux_heater = auxiliary_heater_size * 0.05  # Simplified auxiliary heater fuel cost

        total_cost += cost_grid + cost_aux_heater

        # Exergy efficiency (HCPVT contribution)
        exergy_efficiency = (total_electricity_hcpvt + total_heat_hcpvt) / (hcpvt_size * 1000)  # Simplified
        total_exergy_efficiency += exergy_efficiency

    # Apply penalties for unmet demands
    penalty = unmet_hydrogen_demand * 1000 + unmet_heat_demand * 500 + unmet_cooling_demand * 500
    total_cost += penalty  # Increase cost for unmet demand

    return total_cost, total_exergy_efficiency


toolbox.register("evaluate", evaluate)

# Run the genetic algorithm
population = toolbox.population(n=50)
algorithms.eaMuPlusLambda(population, toolbox, mu=50, lambda_=100, cxpb=0.6, mutpb=0.3, ngen=50)
