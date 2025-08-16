from django import forms
import re
from django.core.exceptions import ValidationError
import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

# Custom validator for phone number (US format)
def validate_phone_number(value):
    phone_regex = re.compile(r'^\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$')  # Matches formats like (555) 555-5555 or 555-555-5555
    if not phone_regex.match(value):
        raise ValidationError('Enter a valid phone number.')

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100,required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    phone_number = forms.CharField(
        max_length=15,  # Allow space for area code, dashes, etc.
        validators=[validate_phone_number],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '###-###-####'})
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control"}))
    address = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class":"form-control"}))
    message = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control","rows":5}), required=True)
    # Honeypot field — humans never see this
    website = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
        label="Leave empty",
    )
    turnstile_token = forms.CharField(widget=forms.HiddenInput())
    
    SPAM_KEYWORDS = [
        "watch this", "unsubscribe",
        "goldsolutions.pro", "click here"
    ]
    
    def clean(self):
        cleaned_data = super().clean()
        
         # 1. Honeypot check
        if cleaned_data.get("website"):
            raise forms.ValidationError("Spam detected (honeypot).")

        # 2. Keyword spam check
        msg = cleaned_data.get("message", "").lower()
        if any(word in msg for word in self.SPAM_KEYWORDS):
            raise forms.ValidationError("Message appears to be spam.")
        
        token = cleaned_data.get("turnstile_token")

        secret_key = settings.TURNSTILE_SECRET_KEY

        response = requests.post(
            "https://challenges.cloudflare.com/turnstile/v0/siteverify",
            data={
                "secret": secret_key,
                "response": token
            }
        )

        result = response.json()
        
        print("CLOUDFLARE RESULT:", result)


        #👇 Log everything returned from Cloudflare
        logger.info("Turnstile result: %s", result)

        if not result.get("success"):
            raise forms.ValidationError("Captcha validation failed. Please try again.")

        # 2. OPTIONAL: fail if hostname does not match your domain
        expected_hostname = "beavershomes.com"
        if result.get("hostname") not in (expected_hostname, "127.0.0.1", "localhost"):
            raise forms.ValidationError("Invalid captcha hostname.")

        # 3. OPTIONAL: use score only if present
        score = result.get("score")
        if score is not None and score < 0.2:
            raise forms.ValidationError("Failed spam score. Submission rejected.")

        return cleaned_data
