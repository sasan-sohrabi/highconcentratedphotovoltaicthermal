def hydrogen_tank_simulation_for_hour(hour, hourly_hydrogen_production, hourly_hydrogen_demand, hydrogen_storage,
                                      max_tank_capacity):
    """
    Simulate hydrogen storage for a given hour, handling hydrogen production, storage, and consumption.
    This simulation follows the four conditions for hydrogen storage:
    1. First hour of the first day.
    2. Each subsequent hour of the first day.
    3. First hour of every subsequent day.
    4. Other hours of other days.

    The maximum storage capacity condition is also applied at every step.

    :param hour: Current hour number of the year (from 0 to 8760)
    :param hourly_hydrogen_production: Hydrogen production at hour t (kg).
    :param hourly_hydrogen_demand: Hydrogen demand at hour t (kg).
    :param hydrogen_storage: Current amount of hydrogen in the tank (kg).
    :param max_tank_capacity: Maximum storage capacity of the tank (kg).
    :return: A dictionary with updated hydrogen storage, unmet demand, and hydrogen supplied for the current hour.
    """

    day = hour // 24 + 1  # Track the day number (1 to 365)
    hour_of_day = hour % 24  # Track the hour of the day (0-23)

    hydrogen_supplied = 0
    unmet_hydrogen_demand = 0

    # Condition 1: First hour of the first day
    if day == 1 and hour_of_day == 0:
        hydrogen_supplied = min(hydrogen_storage, hourly_hydrogen_demand)
        hydrogen_storage -= hydrogen_supplied
        unmet_hydrogen_demand = max(0, hourly_hydrogen_demand - hydrogen_supplied)

    # Condition 2: Each subsequent hour of the first day
    elif day == 1 and hour_of_day > 0:
        hydrogen_storage += hourly_hydrogen_production  # Add hydrogen produced
        hydrogen_storage = min(hydrogen_storage, max_tank_capacity)  # Ensure storage doesn't exceed max capacity
        hydrogen_supplied = min(hydrogen_storage, hourly_hydrogen_demand)
        hydrogen_storage -= hydrogen_supplied
        unmet_hydrogen_demand = max(0, hourly_hydrogen_demand - hydrogen_supplied)

    # Condition 3: First hour of every subsequent day
    elif hour_of_day == 0 and day > 1:
        hydrogen_storage += hourly_hydrogen_production  # Add hydrogen produced
        hydrogen_storage = min(hydrogen_storage, max_tank_capacity)  # Ensure storage doesn't exceed max capacity
        hydrogen_supplied = min(hydrogen_storage, hourly_hydrogen_demand)
        hydrogen_storage -= hydrogen_supplied
        unmet_hydrogen_demand = max(0, hourly_hydrogen_demand - hydrogen_supplied)

    # Condition 4: Other hours of other days
    else:
        hydrogen_storage += hourly_hydrogen_production  # Add hydrogen produced
        hydrogen_storage = min(hydrogen_storage, max_tank_capacity)  # Ensure storage doesn't exceed max capacity
        hydrogen_supplied = min(hydrogen_storage, hourly_hydrogen_demand)
        hydrogen_storage -= hydrogen_supplied
        unmet_hydrogen_demand = max(0, hourly_hydrogen_demand - hydrogen_supplied)

    return {
        'updated_hydrogen_storage': hydrogen_storage,
        'unmet_hydrogen_demand': unmet_hydrogen_demand,
        'hydrogen_supplied': hydrogen_supplied
    }
