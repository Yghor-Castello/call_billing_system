import pytest

from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from billing.models import CallRecord


@pytest.fixture
def api_client():
    client = APIClient()
    user = User.objects.create_user(username="testuser", password="password123")
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


@pytest.mark.django_db
def test_call_record_view_create_start_record(api_client):
    data = {
        'call_id': '123',
        'type': 'start',
        'timestamp': '2023-11-18T10:00:00Z',
        'source': '11987654321',
        'destination': '11912345678',
    }
    response = api_client.post(reverse('call-records'), data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert CallRecord.objects.count() == 1


@pytest.mark.django_db
def test_call_record_view_create_end_record(api_client):
    data = {
        'call_id': '123',
        'type': 'end',
        'timestamp': '2023-11-18T10:30:00Z',
    }
    response = api_client.post(reverse('call-records'), data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert CallRecord.objects.count() == 1


@pytest.mark.django_db
def test_call_record_view_invalid_data(api_client):
    data = {
        'call_id': '123',
        'type': 'start',
        'source': '11987654321',
        'destination': '11912345678',
    }
    response = api_client.post(reverse('call-records'), data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'timestamp' in response.data


@pytest.mark.django_db
def test_phone_bill_view_no_phone_number(api_client):
    response = api_client.get(reverse('phone-bills'))
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['error'] == 'Phone number is required.'


@pytest.mark.django_db
def test_phone_bill_view_invalid_period(api_client):
    response = api_client.get(reverse('phone-bills'), {'phone_number': '11987654321', 'period': 'invalid-period'})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['error'] == 'Invalid period format. Use YYYY-MM.'


@pytest.mark.django_db
def test_phone_bill_view_no_start_record(api_client):
    CallRecord.objects.create(
        call_id='123',
        type='end',
        timestamp='2023-10-10T15:10:00Z',
    )

    response = api_client.get(reverse('phone-bills'), {'phone_number': '11987654321', 'period': '2023-10'})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['call_records']) == 0


@pytest.mark.django_db
def test_phone_bill_view_source_mismatch(api_client):
    CallRecord.objects.create(
        call_id='123',
        type='start',
        timestamp='2023-10-10T15:00:00Z',
        source='11987654322',
        destination='11912345678',
    )
    CallRecord.objects.create(
        call_id='123',
        type='end',
        timestamp='2023-10-10T15:10:00Z',
    )

    response = api_client.get(reverse('phone-bills'), {'phone_number': '11987654321', 'period': '2023-10'})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['call_records']) == 0


@pytest.mark.django_db
def test_phone_bill_view_naive_timestamps(api_client):
    start_time = datetime(2023, 10, 10, 15, 0, 0)
    end_time = datetime(2023, 10, 10, 15, 10, 0)   

    CallRecord.objects.create(
        call_id='123',
        type='start',
        timestamp=start_time,
        source='11987654321',
        destination='11912345678',
    )
    CallRecord.objects.create(
        call_id='123',
        type='end',
        timestamp=end_time,
    )

    response = api_client.get(reverse('phone-bills'), {'phone_number': '11987654321', 'period': '2023-10'})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['call_records']) == 1 


@pytest.mark.django_db
def test_phone_bill_view_valid_request(api_client):
    CallRecord.objects.create(
        call_id='123',
        type='start',
        timestamp='2023-10-10T15:00:00Z',
        source='11987654321',
        destination='11912345678',
    )
    CallRecord.objects.create(
        call_id='123',
        type='end',
        timestamp='2023-10-10T15:10:00Z',
    )

    response = api_client.get(reverse('phone-bills'), {'phone_number': '11987654321', 'period': '2023-10'})
    assert response.status_code == status.HTTP_200_OK
    assert response.data['phone_number'] == '11987654321'
    assert len(response.data['call_records']) == 1