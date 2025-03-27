from django.db import models
from django.contrib.auth.models import User

class BusinessInquiry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    address = models.TextField()
    business_name = models.CharField(max_length=255)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    is_admin_created = models.BooleanField(default=False)  # New field

    def __str__(self):
        return f"{self.name} - {self.status}"
