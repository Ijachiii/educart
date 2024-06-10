from rest_framework import serializers
from .models import *


class ReceiptUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankTransferReceipt
        fields = "__all__"
