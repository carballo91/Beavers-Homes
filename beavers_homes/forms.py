from django import forms
import re
from django.core.exceptions import ValidationError

# Custom validator for phone number (US format)
def validate_phone_number(value):
    phone_regex = re.compile(r'^\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$')  # Matches formats like (555) 555-5555 or 555-555-5555
    if not phone_regex.match(value):
        raise ValidationError('Enter a valid phone number.')

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100,required=True, widget=forms.TextInput(attrs={"placeholder": "Enter your name", "class":"form-control"}))
    phone_number = forms.CharField(
        max_length=15,  # Allow space for area code, dashes, etc.
        validators=[validate_phone_number],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number: 555-555-5555'})
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Enter your email", "class":"form-control"}))
    address = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Enter your address", "class":"form-control"}))
    message = forms.CharField(widget=forms.Textarea(attrs={"placeholder":"Enter your message", "class":"form-control","rows":5}), required=True)