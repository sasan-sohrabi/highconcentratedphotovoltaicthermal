def monthly_scaling_factors():
    """
    :return: List of scaling factors for each month.
    """
    # Example scaling factors: higher in summer (June, July, August), lower in winter
    scaling_factors = {
        1: 0.8,   # January
        2: 0.75,  # February
        3: 0.85,  # March
        4: 0.95,  # April
        5: 1.0,   # May
        6: 1.2,   # June
        7: 1.3,   # July
        8: 1.25,  # August
        9: 1.1,   # September
        10: 1.0,  # October
        11: 0.9,  # November
        12: 0.85  # December
    }
    return scaling_factors

def hourly_demand_profile(is_weekday=True):
    """
    Define hourly hydrogen demand profile for weekdays and weekends.
    :param is_weekday: Boolean flag to determine if it's a weekday.
    :return: List of hourly hydrogen demands for 24 hours.
    """
    if is_weekday:
        # Higher demand during peak hours: morning (6-9 AM) and evening (5-8 PM)
        return [10] * 6 + [50] * 3 + [30] * 8 + [60] * 3 + [10] * 4
    else:
        # Lower demand throughout the weekend
        return [5] * 7 + [20] * 5 + [15] * 6 + [10] * 6


def hydrogen_demand_profile_8760():
    """
    Generate hydrogen demand for 8760 hours, factoring in monthly scaling and weekday/weekend differences.
    :return: List of hourly hydrogen demand for each of the 8760 hours in a year.
    """
    hourly_demand = []
    scaling_factors = monthly_scaling_factors()

    # Get the weekday and weekend demand profiles
    weekday_profile = hourly_demand_profile(is_weekday=True)
    weekend_profile = hourly_demand_profile(is_weekday=False)

    # Define the number of days in each month
    days_in_month = {
        1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
    }

    # Iterate through each month and apply the appropriate scaling factor and weekday/weekend profile
    for month in range(1, 13):
        scaling_factor = scaling_factors[month]
        for day in range(1, days_in_month[month] + 1):
            # Determine if it's a weekday (Monday-Friday) or weekend (Saturday-Sunday)
            day_of_week = (len(hourly_demand) // 24) % 7  # 0=Monday, 6=Sunday
            if day_of_week < 5:
                # Weekday
                daily_profile = [hour * scaling_factor for hour in weekday_profile]
            else:
                # Weekend
                daily_profile = [hour * scaling_factor for hour in weekend_profile]

            # Add the hourly demand for this day
            hourly_demand.extend(daily_profile)

    # If we don't have exactly 8760 hours, fill any remaining hours with the holiday profile
    while len(hourly_demand) < 8760:
        hourly_demand.append(5)  # Assume holiday demand (very low)

    return hourly_demand

