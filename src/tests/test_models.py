import pytest
from decimal import Decimal
from datetime import datetime, date

from django.utils.timezone import make_aware
from django.core.exceptions import ValidationError

from billing.models import CallRecord, PhoneBill, CallDetail


@pytest.mark.django_db
def test_call_record_creation():
    # Test valid 'start' record
    call_record = CallRecord(
        call_id='123',
        type='start',
        timestamp='2023-11-18T10:00:00Z',
        source='11987654321',
        destination='11912345678',
    )
    call_record.full_clean()
    call_record.save()
    assert call_record.call_id == '123'
    assert call_record.type == 'start'
    assert call_record.source == '11987654321'
    assert call_record.destination == '11912345678'
    assert str(call_record) == 'Call 123 - start'

    # Test valid 'end' record (without source and destination)
    call_record_end = CallRecord(
        call_id='123',
        type='end',
        timestamp='2023-11-18T10:10:00Z',
    )
    call_record_end.full_clean()
    call_record_end.save()
    assert call_record_end.type == 'end'
    assert call_record_end.source is None
    assert call_record_end.destination is None
    assert str(call_record_end) == 'Call 123 - end'

    # Test invalid 'start' record without source
    with pytest.raises(ValidationError) as excinfo:
        invalid_record = CallRecord(
            call_id='124',
            type='start',
            timestamp='2023-11-18T11:00:00Z',
        )
        invalid_record.full_clean()
    assert "Source and destination are required" in str(excinfo.value)


@pytest.mark.django_db
def test_phone_bill_creation():
    # Cria uma instância válida de PhoneBill
    phone_bill = PhoneBill(
        phone_number='11987654321',
        period_start=date(2023, 11, 1),
        period_end=date(2023, 11, 30),
        total_price=Decimal('15.00')
    )
    phone_bill.full_clean()  # Executa as validações personalizadas
    phone_bill.save()
    assert phone_bill.phone_number == '11987654321'
    assert phone_bill.period_start == date(2023, 11, 1)
    assert phone_bill.period_end == date(2023, 11, 30)
    assert phone_bill.total_price == Decimal('15.00')
    # Testa o método __str__
    assert str(phone_bill) == 'Bill for 11987654321 - 2023-11'

    # Testa a criação de um PhoneBill inválido
    with pytest.raises(ValidationError) as excinfo:
        invalid_phone_bill = PhoneBill(
            phone_number='11987654321',
            period_start=date(2023, 11, 30),
            period_end=date(2023, 11, 1),  # period_end antes de period_start
            total_price=Decimal('15.00')
        )
        invalid_phone_bill.full_clean()  # Deve levantar ValidationError
    assert "The end of the period must be after the start." in str(excinfo.value)


@pytest.mark.django_db
def test_call_detail_creation():
    # Create a valid phone bill
    phone_bill = PhoneBill(
        phone_number='11987654321',
        period_start=date(2023, 11, 1),
        period_end=date(2023, 11, 30),
        total_price=Decimal('15.00')
    )
    phone_bill.full_clean()
    phone_bill.save()

    # Create a valid call detail
    start_time = make_aware(datetime(2023, 11, 18, 10, 0, 0))
    end_time = make_aware(datetime(2023, 11, 18, 10, 10, 0))
    call_detail = CallDetail(
        phone_bill=phone_bill,
        destination='11912345678',
        start_time=start_time,
        end_time=end_time,
        price=Decimal('2.00')
    )
    call_detail.full_clean()  # Agora deve passar sem erros
    call_detail.save()
    assert call_detail.phone_bill == phone_bill
    assert call_detail.destination == '11912345678'
    assert call_detail.start_time == start_time
    assert call_detail.end_time == end_time
    assert call_detail.duration == end_time - start_time  # Verifica o cálculo de duração
    assert call_detail.price == Decimal('2.00')
    assert str(call_detail) == f'Call to {call_detail.destination} on {start_time.date()}'

    # Test invalid call detail with start_time >= end_time
    with pytest.raises(ValidationError) as excinfo:
        invalid_detail = CallDetail(
            phone_bill=phone_bill,
            destination='11912345678',
            start_time=end_time,
            end_time=start_time,  # End time antes de start time
            price=Decimal('1.50')
        )
        invalid_detail.full_clean()
    assert "The end time must be after the start time." in str(excinfo.value)