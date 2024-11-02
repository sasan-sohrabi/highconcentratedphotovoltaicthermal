import numpy as np

# Constants and Parameters
PV_CAPACITY = 400  # kW, rated PV capacity per unit
WIND_CAPACITY = 300  # kW, rated wind turbine capacity per unit
ELECTROLYZER_EFFICIENCY = 0.8  # 80% efficiency
HYDROGEN_CONSUMPTION_RATE = 0.0076  # kg/km, FCEV hydrogen consumption
DAILY_DISTANCE = 50  # km, daily travel distance per FCEV
TANK_CAPACITY = 1000  # kg, hydrogen storage capacity
COMPRESSOR_EFFICIENCY = 0.75  # Compressor efficiency

# Simulation period (one year, 8760 hours)
HOURS = 8760

# Placeholder hourly data (random values representing typical profiles)
np.random.seed(0)
hourly_solar_radiation = np.clip(np.sin(np.linspace(0, 2 * np.pi, HOURS)) + np.random.normal(0, 0.1, HOURS), 0, 1)
hourly_wind_speed = np.clip(0.5 + 0.5 * np.sin(np.linspace(0, 4 * np.pi, HOURS)) + np.random.normal(0, 0.1, HOURS), 0,
                            1)


# Functions for each component model

def pv_generation(hour):
    """ Simulate PV generation based on solar radiation and PV capacity. """
    return PV_CAPACITY * hourly_solar_radiation[hour]


def wind_generation(hour):
    """ Simulate wind generation based on wind speed and turbine capacity. """
    return WIND_CAPACITY * hourly_wind_speed[hour]


def hydrogen_production(energy_available):
    """ Calculate hydrogen production from available energy, considering electrolyzer efficiency. """
    return ELECTROLYZER_EFFICIENCY * energy_available / 39.4  # kWh/kg of hydrogen


def compressor_energy(hydrogen_mass):
    """ Calculate compressor energy required to pressurize hydrogen for storage. """
    return (1 / COMPRESSOR_EFFICIENCY) * hydrogen_mass * 2.5  # Example energy per kg to compress


# System simulation
total_hydrogen_produced = 0
storage = 0
hourly_hydrogen_demand = DAILY_DISTANCE * HYDROGEN_CONSUMPTION_RATE

# Array to store results for analysis
hourly_results = {
    "Hour": [],
    "PV_Generation": [],
    "Wind_Generation": [],
    "Energy_Available": [],
    "Hydrogen_Produced": [],
    "Storage_Level": [],
    "Demand": [],
    "Shortfall": [],
}

for hour in range(HOURS):
    # Generate power from PV and Wind
    pv_power = pv_generation(hour)
    wind_power = wind_generation(hour)
    energy_available = pv_power + wind_power

    # Calculate hydrogen production and compression energy
    hydrogen_produced = hydrogen_production(energy_available)
    compression_energy = compressor_energy(hydrogen_produced)

    # Update storage and account for demand
    storage += hydrogen_produced - hourly_hydrogen_demand
    shortfall = max(0, hourly_hydrogen_demand - storage)
    storage = max(0, storage)  # Prevent negative storage levels

    # Record results
    hourly_results["Hour"].append(hour)
    hourly_results["PV_Generation"].append(pv_power)
    hourly_results["Wind_Generation"].append(wind_power)
    hourly_results["Energy_Available"].append(energy_available)
    hourly_results["Hydrogen_Produced"].append(hydrogen_produced)
    hourly_results["Storage_Level"].append(storage)
    hourly_results["Demand"].append(hourly_hydrogen_demand)
    hourly_results["Shortfall"].append(shortfall)

# Calculate summary statistics for validation of storage and hydrogen production
total_hydrogen_produced = np.sum(hourly_results["Hydrogen_Produced"])
total_shortfall = np.sum(hourly_results["Shortfall"])

total_hydrogen_produced, total_shortfall
