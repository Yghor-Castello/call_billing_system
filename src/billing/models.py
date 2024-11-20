from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


# Validator for phone number format
phone_regex = RegexValidator(
    regex=r"^\d{2}\d{8,9}$",
    message="Phone number must be in the format AAXXXXXXXXX.",
)

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
        indexes = [
            models.Index(fields=["call_id"]),
            models.Index(fields=["type"]),
            models.Index(fields=["timestamp"]),
        ]
        unique_together = ("call_id", "type")

    def clean(self):
        if self.type == "start":
            if not self.source or not self.destination:
                raise ValidationError("Source and destination are required for 'start' records.")
        super().clean()

    def __str__(self):
        return f"Call {self.call_id} - {self.type}"


class PhoneBill(models.Model):
    phone_number = models.CharField(max_length=11)
    period_start = models.DateField()
    period_end = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        indexes = [
            models.Index(fields=["phone_number"]),
            models.Index(fields=["period_start", "period_end"]),
        ]

    def clean(self):
        """
        Ensure that the end period is after the start period.
        """
        if self.period_end <= self.period_start:
            raise ValidationError("The end of the period must be after the start.")


    def __str__(self):
        return f"Bill for {self.phone_number} - {self.period_start.strftime('%Y-%m')}"


class CallDetail(models.Model):
    phone_bill = models.ForeignKey(PhoneBill, related_name="call_details", on_delete=models.CASCADE)
    destination = models.CharField(max_length=11)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.DurationField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        indexes = [
            models.Index(fields=["destination"]),
            models.Index(fields=["start_time", "end_time"]),
        ]
    
    def clean(self):
        """
        Validates the CallDetail instance.

        Ensures that the `end_time` is greater than `start_time`, raising a 
        ValidationError if this condition is not met. Additionally, calculates 
        the `duration` field as the difference between `end_time` and `start_time`.
        """
        if self.end_time <= self.start_time:
            raise ValidationError("The end time must be after the start time.")
        self.duration = self.end_time - self.start_time

    def full_clean(self, exclude=None, validate_unique=True, validate_constraints=True):
        """
        Performs full validation on the CallDetail instance.

        This method overrides the default `full_clean` to exclude the `duration` 
        field from validation. The `duration` field is dynamically calculated 
        in the `clean` method and does not need validation as part of 
        the regular `clean_fields` process.
        """
        exclude = exclude or set()
        exclude.add('duration')
        super().full_clean(exclude=exclude, validate_unique=validate_unique, validate_constraints=validate_constraints)

    def __str__(self):
        return f"Call to {self.destination} on {self.start_time.date()}"