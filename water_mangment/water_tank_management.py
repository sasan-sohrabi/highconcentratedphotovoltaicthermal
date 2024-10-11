def water_tank_management(water_produced, water_consumed, previous_storage, max_storage_capacity):
    """
    Simulate the water tank storage, tracking water produced by MED and consumed by the electrolyzer.
    :param water_produced: Water produced by MED desalination (kg).
    :param water_consumed: Water consumed by the electrolyzer (kg).
    :param previous_storage: Water stored in the tank from the previous hour (kg).
    :param max_storage_capacity: Maximum capacity of the water tank (kg).
    :return: Water storage after the hour, water deficit (if any).
    """
    water_balance = previous_storage + water_produced - water_consumed
    if water_balance >= max_storage_capacity:
        water_storage = max_storage_capacity
        water_deficit = 0
    elif water_balance < 0:
        water_storage = 0
        water_deficit = -water_balance
    else:
        water_storage = water_balance
        water_deficit = 0
    return water_storage, water_deficit