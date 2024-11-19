from rest_framework import serializers

from .models import CallRecord


class CallRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallRecord
        fields = ["id", "call_id", "type", "timestamp", "source", "destination"]


class CallDetailSerializer(serializers.Serializer):
    destination = serializers.CharField(max_length=11)
    call_start_date = serializers.DateField()
    call_start_time = serializers.TimeField()
    duration = serializers.CharField()
    price = serializers.CharField()


class PhoneBillSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)
    period = serializers.CharField()
    total_price = serializers.CharField()
    call_records = CallDetailSerializer(many=True)