from django.contrib import admin

from .models import (
    CallRecord, 
    PhoneBill, 
    CallDetail
)


admin.site.register(CallRecord)
admin.site.register(PhoneBill)
admin.site.register(CallDetail)