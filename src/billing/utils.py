from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, time, timedelta
from django.utils.timezone import make_aware, get_current_timezone


def calculate_call_price(start_time, end_time):
    """
    Calculate the price of a call based on start and end times.
    Ensures that all datetime objects are timezone-aware.
    """
    current_tz = get_current_timezone()

    # Make both start_time and end_time timezone-aware if they are not already
    if start_time.tzinfo is None:
        start_time = make_aware(start_time, current_tz)
    if end_time.tzinfo is None:
        end_time = make_aware(end_time, current_tz)

    fixed_rate = Decimal('0.36')
    rate_per_minute = Decimal('0.09')
    total_price = fixed_rate
    total_billable_minutes = 0

    current_time = start_time

    while current_time < end_time:
        if time(6, 0) <= current_time.time() < time(22, 0):
            # Calculate the end of the standard tariff period
            end_of_standard_tariff = datetime.combine(
                current_time.date(), time(22, 0)
            ).astimezone(current_tz)
            period_end = min(end_of_standard_tariff, end_time)
            duration_seconds = (period_end - current_time).total_seconds()
            minutes = int(duration_seconds // 60)
            total_billable_minutes += minutes
            current_time = period_end
        else:
            # Calculate the start of the next standard tariff period
            if current_time.time() >= time(22, 0):
                next_standard_tariff = datetime.combine(
                    current_time.date() + timedelta(days=1), time(6, 0)
                ).astimezone(current_tz)
            else:
                next_standard_tariff = datetime.combine(
                    current_time.date(), time(6, 0)
                ).astimezone(current_tz)
            current_time = min(next_standard_tariff, end_time)

    total_price += total_billable_minutes * rate_per_minute
    total_price = total_price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return total_price


def format_duration(duration):
    total_seconds = int(duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours}h{minutes}m{seconds}s"