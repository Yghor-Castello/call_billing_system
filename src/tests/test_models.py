import pytest
from decimal import Decimal
from django.utils.timezone import make_aware
from datetime import datetime, date, timedelta

from billing.models import CallRecord, PhoneBill, CallDetail


@pytest.mark.django_db
def test_call_record_creation():
    call_record = CallRecord.objects.create(
        call_id='123',
        type='start',
        timestamp='2023-11-18T10:00:00Z',
        source='11987654321',
        destination='11912345678',
    )
    assert call_record.call_id == '123'
    assert call_record.type == 'start'
    assert call_record.source == '11987654321'
    assert call_record.destination == '11912345678'
    # Test __str__ method
    assert str(call_record) == 'Call 123 - start'


@pytest.mark.django_db
def test_phone_bill_creation():
    phone_bill = PhoneBill.objects.create(
        phone_number='11987654321',
        period_start=date(2023, 11, 1),
        period_end=date(2023, 11, 30),
        total_price=Decimal('15.00')
    )
    assert phone_bill.phone_number == '11987654321'
    assert phone_bill.period_start == date(2023, 11, 1)
    assert phone_bill.period_end == date(2023, 11, 30)
    assert phone_bill.total_price == Decimal('15.00')
    # Test __str__ method
    assert str(phone_bill) == 'Bill for 11987654321 - 2023-11'


@pytest.mark.django_db
def test_call_detail_creation():
    phone_bill = PhoneBill.objects.create(
        phone_number='11987654321',
        period_start=date(2023, 11, 1),
        period_end=date(2023, 11, 30),
        total_price=Decimal('15.00')
    )
    start_time = make_aware(datetime(2023, 11, 18, 10, 0, 0))
    end_time = make_aware(datetime(2023, 11, 18, 10, 10, 0))
    duration = end_time - start_time
    call_detail = CallDetail.objects.create(
        phone_bill=phone_bill,
        destination='11912345678',
        start_time=start_time,
        end_time=end_time,
        duration=duration,
        price=Decimal('2.00')
    )
    assert call_detail.phone_bill == phone_bill
    assert call_detail.destination == '11912345678'
    assert call_detail.start_time == start_time
    assert call_detail.end_time == end_time
    assert call_detail.duration == duration
    assert call_detail.price == Decimal('2.00')
    # Test __str__ method
    assert str(call_detail) == f'Call to 11912345678 on {start_time.date()}'