from django import forms
from .models import BusinessInquiry

class BusinessInquiryForm(forms.ModelForm):
    class Meta:
        model = BusinessInquiry
        fields = ['name', 'mobile', 'address', 'business_name']  # username, password HATADIYA
