from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('about/',views.about, name="about"),
    path('gallery', views.gallery, name="gallery"),
    path('contact', views.contact, name="contact"),
    path('sitemap.xml',views.sitemap,name='sitemap'),
    path('robots.txt', views.robots_txt,name='robots_text')
]