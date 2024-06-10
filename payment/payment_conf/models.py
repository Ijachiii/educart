from django.db import models
import datetime

# Create your models here.
class BankTransferReceipt(models.Model):
    receipt = models.FileField(upload_to="receipt/")
    order_id = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)
    # date = models.DateTimeField()

    def __str__(self): 
        return self.order_id