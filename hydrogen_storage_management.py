def hydrogen_storage_management(hydrogen_produced, hydrogen_consumed, previous_storage, max_storage_capacity):
    """
    Simulate hydrogen storage management.
    :param hydrogen_produced: Hydrogen produced by the electrolyzer (kg).
    :param hydrogen_consumed: Hydrogen consumed (kg).
    :param previous_storage: Hydrogen stored in the tank from the previous hour (kg).
    :param max_storage_capacity: Maximum capacity of the hydrogen tank (kg).
    :return: Hydrogen storage after the hour.
    """
    hydrogen_balance = previous_storage + hydrogen_produced - hydrogen_consumed
    if hydrogen_balance >= max_storage_capacity:
        hydrogen_storage = max_storage_capacity
        hydrogen_excess = hydrogen_balance - max_storage_capacity
    else:
        hydrogen_storage = hydrogen_balance
        hydrogen_excess = 0
    return hydrogen_storage, hydrogen_excess
