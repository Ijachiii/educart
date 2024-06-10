from django.urls import path
from .views import *

urlpatterns = [
    path("", NewsletterView.as_view(), name="newsletter")
]