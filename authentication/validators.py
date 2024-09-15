from datetime import date
from rest_framework import serializers


def validate_dob(dob):
    """Check if the user is at least 18 years old."""
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    if age < 18:
        raise serializers.ValidationError("You must be at least 18 years old.")

    return dob
