from django.shortcuts import render, redirect
from django.http import request, HttpResponse
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
import os
from datetime import datetime

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
    return render(request, "beavers_homes/contact.html", {"form":form,"TURNSTILE_SITE_KEY": settings.TURNSTILE_SITE_KEY})

def sitemap(request):
    """
    Generates a sitemap.xml for search engines.
    """

    # List of static pages (named url pattern, change frequency, priority)
    static_pages = [
        ("index", "weekly", "1.0"),
        ("about", "yearly", "0.8"),
        ("gallery", "monthly", "0.8"),
        ("contact", "yearly", "0.7"),
    ]

    lastmod = datetime.utcnow().date().isoformat()
    xml_parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]

    for name, changefreq, priority in static_pages:
        loc = request.build_absolute_uri(reverse(name))
        print(f"loc: {loc}")
        xml_parts.append("  <url>")
        xml_parts.append(f"    <loc>{loc}</loc>")
        xml_parts.append(f"    <lastmod>{lastmod}</lastmod>")
        xml_parts.append(f"    <changefreq>{changefreq}</changefreq>")
        xml_parts.append(f"    <priority>{priority}</priority>")
        xml_parts.append("  </url>")

    xml_parts.append("</urlset>")

    sitemap_xml = "\n".join(xml_parts)
    return HttpResponse(sitemap_xml, content_type="application/xml")

def robots_txt(request):
    """
    Serve robots.txt
    """
    lines = [
        "User-Agent: *",
        "Disallow: /admin/",
        "Sitemap: https://www.beavershomesllc.com/sitemap.xml"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
