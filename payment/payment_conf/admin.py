from django.contrib import admin
from .models import *

# Register your models here.
class BankTransferReceiptAdmin(admin.ModelAdmin):
    model = BankTransferReceipt
    list_display = ["order_id", "receipt", "date"]

admin.site.register(BankTransferReceipt, BankTransferReceiptAdmin)