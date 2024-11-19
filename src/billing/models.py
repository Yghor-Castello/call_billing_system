from django.db import models
from django.utils.timezone import now


class CallRecord(models.Model):
    RECORD_TYPE_CHOICES = [
        ("start", "Start"),
        ("end", "End"),
    ]

    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=5, choices=RECORD_TYPE_CHOICES)
    timestamp = models.DateTimeField()
    call_id = models.CharField(max_length=50)
    source = models.CharField(max_length=11, null=True, blank=True)
    destination = models.CharField(max_length=11, null=True, blank=True)

    class Meta:
        unique_together = ("call_id", "type")

    def __str__(self):
        return f"Call {self.call_id} - {self.type}"


class PhoneBill(models.Model):
    phone_number = models.CharField(max_length=11)
    period_start = models.DateField()  # Início do período (mês/ano)
    period_end = models.DateField()  # Fim do período (gerado automaticamente)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Bill for {self.phone_number} - {self.period_start.strftime('%Y-%m')}"


class CallDetail(models.Model):
    phone_bill = models.ForeignKey(PhoneBill, related_name="call_details", on_delete=models.CASCADE)
    destination = models.CharField(max_length=11)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.DurationField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Call to {self.destination} on {self.start_time.date()}"