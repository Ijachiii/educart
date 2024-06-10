from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
import uuid
import hashlib
from django.db.models.signals import pre_save
from django.dispatch import receiver
from cryptography.fernet import Fernet
import base64
import datetime


# Create your models here.    
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password./
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    USER_TYPES = (
        ("user", "User"),
        ("consultant", "Consultant"),
        ("institution", "Institution"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    username = None
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    profile_picture = models.ImageField(upload_to="profile_picture/", blank=True, null=True)
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    country_of_residence = models.CharField(max_length=256)
    institution_of_study = models.CharField(max_length=100, null=True, blank=True)
    country_code = models.IntegerField(default=234)
    phone_number = models.CharField(max_length=10, unique=True, blank=False)
    country_of_birth = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=256, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)

    is_verified = models.BooleanField(default=False)
    is_restricted = models.BooleanField(default=False)
    wallet_id = models.CharField(max_length=10, unique=True, null=True)

    free_consultation = models.BooleanField(default=True)
    profile_completed = models.BooleanField(default=False)

    otp = models.CharField(max_length=4, blank=True, null=True)
    otp_verified = models.BooleanField(default=False)
    otp_expiry = models.DateTimeField(blank=True, null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    

class Consultant(models.Model):
    user = models.OneToOneField(CustomUser, related_name="consultant", on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="profile_picture/", blank=True, null=True)
    name = models.CharField(max_length=256)
    price_per_hour = models.IntegerField()
    specialization = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    bio = models.TextField()
    years_of_experience = models.IntegerField()
    state = models.CharField(max_length=256)
    country = models.CharField(max_length=256)

    def __str__(self):
        return self.user.email
    

class OrderHistory(models.Model):
    user = models.ForeignKey(CustomUser, related_name="order_history", on_delete=models.CASCADE)
    order_id = models.CharField(max_length=50)
    order_type = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)

    def __str__(self): 
        return self.order_id



class OrderHistoryGuest(models.Model):
    order_id = models.CharField(max_length=50)
    order_type = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)

    def __str__(self): 
        return self.order_id



# class AddressBook(models.Model):
#     user = models.ForeignKey(CustomUser, related_name="addresses", on_delete=models.CASCADE)
#     home_address = models.CharField(max_length=200, null=False, blank=False)
#     city = models.CharField(max_length=256, null=False, blank=False)
#     state = models.CharField(max_length=50, null=False, blank=False)
#     zip_code = models.CharField(max_length=12, null=False, blank=False)
#     country = models.CharField(max_length=256, null=False, blank=False)

#     def __str__(self):
#         return self.user.email


# @receiver(pre_save, sender=CustomUser)
# def hash_transaction_pin(sender, instance, **kwargs):
#     """
#     Signal handler to hash the transaction pin before saving to the database.
#     """
    
#     # Get the transaction pin value from the instance
#     transaction_pin = instance.transaction_pin

#     # Check if transaction pin exists and is not hashed
#     if transaction_pin:
#         # Hash the transaction pin using hashlib
#         hashed_transaction_pin = base64.b64encode(bytes(transaction_pin, "utf-8"))

#         # Set the hashed transaction pin back to the instance
#         instance.transaction_pin = hashed_transaction_pin




# class SecurityQuestions(models.Model):
#     security_question = models.CharField(max_length=256) 

#     def __str__(self):
#         return self.security_question