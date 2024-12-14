from django.shortcuts import render, redirect
from django.http import request, HttpResponse
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
import os

# Create your views here.
def index(request):
    return render(request,"beavers_homes/index.html")

def about(request):
    return render(request,"beavers_homes/about.html")

def gallery(request):
    return render(request, "beavers_homes/gallery.html")

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            phone_number = form.cleaned_data["phone_number"]
            email = form.cleaned_data["email"]
            address = form.cleaned_data["address"]
            message = form.cleaned_data["message"]
            
            subject = "New Contact Form Submission from Beavers Homes Website"
            message = f"""
            Dear Team,

            You have received a new message via the Contact Us form on your website. Below are the details:

            Name: {name}
            Address: {address}
            Email: {email}
            Phone: {phone_number}
            Message:{message}

            Company Contact Information:
            Beavers Homes LLC
            Phone: (937)-231-7652

            Please reach out to the sender promptly.

            Best regards,
            Beavers Homes Website
            """
            recipient_email = os.getenv("EMAIL_HOST_USER")
            if not recipient_email:
                raise ValueError("RECIPIENT_EMAIL environment variable not set")
            
            send_mail(
                subject,  # Subject
                message,                        # Message body
                settings.DEFAULT_FROM_EMAIL,                           # From email
                [recipient_email],     # To email
                fail_silently=False,
            )
                    # Use reverse() to generate the URL and append the query parameter
            url = reverse('contact') + "?success=true"
            
            # Redirect to the contact page with the query parameter
            return redirect(url)
            #return render(request, "beavers_homes/contact.html", {"form":ContactForm(),"message":"Thanks for contacting us!"})
    else:
        form = ContactForm()
    return render(request, "beavers_homes/contact.html", {"form":form})