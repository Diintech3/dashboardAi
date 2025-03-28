from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


def validate_pan_number(value):
    # PAN number ka format: 5 letters + 4 digits + 1 letter (eg. ABCDE1234F)
    pan_regex = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
    if not re.match(pan_regex, value):
        raise ValidationError('Invalid PAN number format.')


class BusinessInquiry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100, default='N/A') 
    mobile = models.CharField(max_length=15, default='0000000000') 
    address = models.TextField(default='No Address Provided') 
    business_name = models.CharField(max_length=255, default='No Business Name') 
    email = models.EmailField(default='example@example.com') 
    gstnumber = models.CharField(max_length=15, unique=True, default='0000000000') 
    pannumber = models.CharField(max_length=10, unique=True, validators=[validate_pan_number], default='AAAAA0000A') 
    category = models.CharField(max_length=50, default='Uncategorized') 
    city = models.CharField(max_length=50, default='Unknown City') 
    pin = models.CharField(max_length=6, default='000000') 
    business_number = models.CharField(max_length=15, unique=True, default='0000000000', blank=True) 

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    is_admin_created = models.BooleanField(default=False)  # Default to False for admin created

    def __str__(self):
        return f"{self.name} - {self.status}"
