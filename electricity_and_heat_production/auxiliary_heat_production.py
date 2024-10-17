def natural_gas_required(mass_water, t1, t2, efficiency, energy_content_gas=10.55):
    """
    Calculate the amount of natural gas required to heat water from t1 to t2.

    :param mass_water: Mass of the water (in kg, 1 liter = 1 kg).
    :param t1: Initial temperature of the water (in °C).
    :param t2: Final temperature of the water (in °C).
    :param efficiency: Efficiency of the natural gas heater (e.g., 0.9 for 90%).
    :param energy_content_gas: Energy content of natural gas (in kWh/m³, default is 10.55 kWh/m³).
    :return: The volume of natural gas required (in cubic meters, m³).
    """
    cp_water = 4.186  # Specific heat capacity of water in kJ/kg°C
    delta_t = t2 - t1  # Temperature difference (°C)

    # Step 1: Calculate the heat required (Q) in kWh
    heat_required_kwh = (mass_water * cp_water * delta_t) / 3600  # Convert kJ to kWh

    # Step 2: Calculate the volume of natural gas required
    natural_gas_volume = heat_required_kwh / (efficiency * energy_content_gas)

    return natural_gas_volume


# Example usage
mass_water = 200  # kg (equivalent to 200 liters)
t1 = 20  # Initial temperature (°C)
t2 = 60  # Final temperature (°C)
efficiency = 0.9  # 90% efficient heater

# Calculate the volume of natural gas required
gas_needed = natural_gas_required(mass_water, t1, t2, efficiency)

# Output result
print(f"Natural gas required: {gas_needed:.2f} m³")
