from django.core.exceptions import ValidationError
from django.utils import timezone

def validate_deadline(value):
    if value < timezone.now():
        raise ValidationError("Deadline must be in the future")