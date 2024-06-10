from django.urls import path
from . import views


urlpatterns = [
    path("upload-receipt/", views.ReceiptUploadView.as_view(), name="upload_receipt"),
]