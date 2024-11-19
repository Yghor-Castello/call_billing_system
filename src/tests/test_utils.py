import pytest
from decimal import Decimal
from datetime import datetime, timedelta
from django.utils.timezone import make_aware

from billing.utils import calculate_call_price, format_duration


def test_calculate_call_price_standard_tariff():
    start_time = make_aware(datetime(2023, 11, 18, 8, 0, 0))
    end_time = make_aware(datetime(2023, 11, 18, 8, 10, 0))
    price = calculate_call_price(start_time, end_time)
    expected_price = Decimal('0.36') + (Decimal('10') * Decimal('0.09'))
    assert price == expected_price, f"Expected {expected_price}, but got {price}"


def test_calculate_call_price_reduced_tariff():
    start_time = make_aware(datetime(2023, 11, 18, 23, 0, 0))
    end_time = make_aware(datetime(2023, 11, 18, 23, 10, 0))
    price = calculate_call_price(start_time, end_time)
    expected_price = Decimal('0.36')
    assert price == expected_price, f"Expected {expected_price}, but got {price}"


def test_calculate_call_price_crossing_tariffs():
    start_time = make_aware(datetime(2023, 11, 18, 21, 59, 0))
    end_time = make_aware(datetime(2023, 11, 18, 22, 1, 0))
    price = calculate_call_price(start_time, end_time)
    expected_price = Decimal('0.36') + (Decimal('1') * Decimal('0.09'))
    assert price == expected_price, f"Expected {expected_price}, but got {price}"


def test_calculate_call_price_entirely_reduced_tariff():
    start_time = make_aware(datetime(2023, 11, 18, 4, 0, 0))
    end_time = make_aware(datetime(2023, 11, 18, 5, 0, 0))
    price = calculate_call_price(start_time, end_time)
    expected_price = Decimal('0.36')
    assert price == expected_price, f"Expected {expected_price}, but got {price}"


def test_calculate_call_price_naive_times():
    start_time = datetime(2023, 11, 18, 8, 0, 0)  
    end_time = datetime(2023, 11, 18, 8, 10, 0)    
    price = calculate_call_price(start_time, end_time)
    expected_price = Decimal('0.36') + (Decimal('10') * Decimal('0.09'))
    assert price == expected_price, f"Expected {expected_price}, but got {price}"


def test_calculate_call_price_after_22():
    start_time = make_aware(datetime(2023, 11, 18, 22, 30, 0))
    end_time = make_aware(datetime(2023, 11, 18, 23, 30, 0))
    price = calculate_call_price(start_time, end_time)
    expected_price = Decimal('0.36')
    assert price == expected_price, f"Expected {expected_price}, but got {price}"


def test_format_duration():
    duration = timedelta(hours=2, minutes=30, seconds=45)
    duration_str = format_duration(duration)
    assert duration_str == '2h30m45s', f"Expected '2h30m45s', but got {duration_str}"