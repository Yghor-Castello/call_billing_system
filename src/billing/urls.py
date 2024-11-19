from django.urls import path

from .views import CallRecordView, PhoneBillView


urlpatterns = [
    path("call-records/", CallRecordView.as_view(), name="call-records"),
    path("phone-bills/", PhoneBillView.as_view(), name="phone-bills"),
]