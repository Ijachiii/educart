from django.db import models
from accounts.models import CustomUser, OrderHistory
from django.utils import timezone
import django

# Create your models here.
class SevisInformationUser(models.Model):
    CATEGORY_CHOICES = (
        ("au pair ($35)", "Au Pair ($35)"),
        ("camp counselor ($35)", "Camp Counselor ($35)"),
        ("summer work/travel ($35)", "Summer Work/Travel ($35)"),
        ("others ($200)", "Others ($200)"),
    )

    # user = models.OneToOneField(CustomUser, related_name="sevis_information", on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name="user_sevis_information", on_delete=models.CASCADE)
    sevis_coupon = models.FileField(upload_to="sevis_coupon/", blank=True, null=True)
    sevis_id = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    given_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    form = models.FileField(upload_to="form/", blank=False, null=False)
    passport = models.ImageField(upload_to="passport/", blank=False, null=False)
    international_passport = models.FileField(upload_to="international_passport/", blank=False, null=False)
    form_type = models.CharField(max_length=100)
    category = models.CharField(max_length=100, null=True, blank=True, choices=CATEGORY_CHOICES)
    email = models.CharField(max_length=100)
    country_of_citizenship = models.CharField(max_length=100)
    country_of_birth = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    street_address_1 = models.CharField(max_length=200)
    street_address_2 = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    sevis_fee = models.CharField(max_length=10, null=True, blank=True, default="350")
    fee_in_dollars = models.CharField(max_length=10, null=True, blank=True)
    fee_in_naira = models.CharField(max_length=10, null=True, blank=True)
    order_id = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=100, null=True, blank=True, default="Payment Pending")

    def __str__(self):
        return self.user.email
    

class SevisInformationGuest(models.Model):
    CATEGORY_CHOICES = (
        ("au pair ($35)", "Au Pair ($35)"),
        ("camp counselor ($35)", "Camp Counselor ($35)"),
        ("summer work/travel ($35)", "Summer Work/Travel ($35)"),
        ("others ($200)", "Others ($200)"),
    )

    sevis_coupon = models.FileField(upload_to="sevis_coupon/", blank=True, null=True)
    sevis_id = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    given_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    form = models.FileField(upload_to="form/", blank=False, null=False)
    international_passport = models.FileField(upload_to="international_passport/", blank=False, null=False)
    form_type = models.CharField(max_length=100)
    category = models.CharField(max_length=100, null=True, blank=True, choices=CATEGORY_CHOICES)
    email = models.CharField(max_length=100)
    country_of_citizenship = models.CharField(max_length=100)
    country_of_birth = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    street_address_1 = models.CharField(max_length=200, null=True, blank=True)
    street_address_2 = models.CharField(max_length=200, null=True, blank=True)
    # country = models.CharField(max_length=200)
    state = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    sevis_fee = models.IntegerField(default=350)
    charges = models.IntegerField(default=35)
    fee_in_dollars = models.IntegerField(null=True, blank=True)
    fee_in_naira = models.IntegerField(null=True, blank=True)
    rate = models.IntegerField(default=700)
    order_id = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=100, null=True, blank=True, default="Payment Pending")

    def __str__(self):
        return self.sevis_id 