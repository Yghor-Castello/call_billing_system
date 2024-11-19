import pytest
from billing.serializers import CallRecordSerializer
from rest_framework.exceptions import ValidationError


@pytest.mark.django_db
def test_call_record_serializer_valid():
    data = {
        'call_id': '123',
        'type': 'start',
        'timestamp': '2023-11-18T10:00:00Z',
        'source': '11987654321',
        'destination': '11912345678',
    }
    serializer = CallRecordSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.validated_data['call_id'] == '123'


@pytest.mark.django_db
def test_call_record_serializer_invalid():
    data = {
        'call_id': '123',
        'type': 'start',
        'timestamp': 'invalid-timestamp',
        'source': '11987654321',
        'destination': '11912345678',
    }
    serializer = CallRecordSerializer(data=data)
    assert not serializer.is_valid()
    assert 'timestamp' in serializer.errors