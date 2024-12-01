from django.shortcuts import render
from django.http import request, HttpResponse
from .forms import ContactForm
from django.core.mail import send_mail

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

            print(name,phone_number,email,address,message)
            
                        # Example: Send an email (you can configure the email backend in settings.py)
            send_mail(
                f'Contact Message from {name}',  # Subject
                message,                        # Message body
                email,                           # From email
                ["carballo.rafael91@gmail.com"],     # To email
                fail_silently=False,
            )
    else:
        form = ContactForm()
    return render(request, "beavers_homes/contact.html", {"form":form})