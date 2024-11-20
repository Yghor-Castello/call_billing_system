from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.timezone import make_aware, get_current_timezone

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import datetime, timedelta

from .models import CallRecord
from .utils import calculate_call_price, format_duration
from .serializers import CallRecordSerializer, PhoneBillSerializer


class CallRecordView(APIView):
    """
    View to create call records (start and end).
    """
    @swagger_auto_schema(
        operation_description="Create a call record (start or end).",
        request_body=CallRecordSerializer,
        responses={
            201: CallRecordSerializer,
            400: "Invalid data provided.",
        },
    )
    def post(self, request):
        serializer = CallRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhoneBillView(APIView):
    """
    View to retrieve phone billing information for a given phone number 
    and billing period.
    """
    @swagger_auto_schema(
        operation_description="Retrieve the phone bill for a given phone number and period.",
        manual_parameters=[
            openapi.Parameter(
                'phone_number',
                openapi.IN_QUERY,
                description="Phone number to fetch the bill for.",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                'period',
                openapi.IN_QUERY,
                description="Billing period in YYYY-MM format.",
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ],
        responses={
            200: PhoneBillSerializer,
            400: "Bad request or invalid parameters.",
        },
    )
    def get(self, request):
        phone_number = request.query_params.get("phone_number")
        period = request.query_params.get("period")

        if not phone_number:
            return Response(
                {"error": "Phone number is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Determine the period
        if period:
            try:
                period_start = datetime.strptime(period, "%Y-%m").date()
            except ValueError:
                return Response(
                    {"error": "Invalid period format. Use YYYY-MM."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            today = datetime.today()
            period_start = (today.replace(day=1) - timedelta(days=1)).replace(day=1).date()

        # Add timezone awareness
        current_tz = get_current_timezone()
        period_start = make_aware(datetime.combine(period_start, datetime.min.time()), current_tz)
        period_end = make_aware(datetime.combine(
            (period_start + timedelta(days=31)).replace(day=1), datetime.min.time()
        ), current_tz)

        # Fetch all end call records that ended in the period
        end_records = CallRecord.objects.filter(
            type="end",
            timestamp__gte=period_start,
            timestamp__lt=period_end,
        )

        total_price = 0
        call_details = []

        for end_record in end_records:
            # Find the corresponding start record
            start_record = CallRecord.objects.filter(
                type="start",
                call_id=end_record.call_id,
            ).first()

            if not start_record:
                continue  # Skip if no start record

            # Ensure the call was made by the phone_number
            if start_record.source != phone_number:
                continue

            start_time = start_record.timestamp
            end_time = end_record.timestamp

            # Ensure start_time and end_time are aware
            if start_time.tzinfo is None:
                start_time = make_aware(start_time, current_tz)
            if end_time.tzinfo is None:
                end_time = make_aware(end_time, current_tz)

            duration = end_time - start_time
            price = calculate_call_price(start_time, end_time)
            duration_str = format_duration(duration)

            call_details.append({
                "destination": start_record.destination,
                "call_start_date": start_time.date(),
                "call_start_time": start_time.time(),
                "duration": duration_str,
                "price": f"R$ {price:.2f}",
            })

            total_price += price

        phone_bill = {
            "phone_number": phone_number,
            "period": period_start.strftime("%Y-%m"),
            "total_price": f"R$ {total_price:.2f}",
            "call_records": call_details,
        }

        serializer = PhoneBillSerializer(phone_bill)
        return Response(serializer.data, status=status.HTTP_200_OK)