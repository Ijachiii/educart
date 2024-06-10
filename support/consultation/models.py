from django.db import models
from accounts.models import CustomUser, Consultant

# Create your models here.
class Consultation(models.Model):
    # CONSULTATION_WAY_CHOICES = (
    #     ("zoom video call", "Zoom Video Call"),
    #     ("phone call", "Phone Call"),
    # )

    # TIME_OF_CONSULTATION_CHOICES = (
    #     ("today", "Today"),
    #     ("later", "Later"),
    # )

    user = models.ForeignKey(CustomUser, related_name="user_consultation", on_delete=models.CASCADE)
    consultant = models.ForeignKey(Consultant, related_name="consultant", on_delete=models.CASCADE, null=True, blank=True)
    consultation = models.CharField(max_length=10000, null=False, blank=False)
    details = models.CharField(max_length=10000, null=False, blank=False)
    consultation_fee = models.IntegerField(blank=True, null=True)
    fee_in_naira = models.IntegerField(blank=True, null=True)
    fee_in_dollars = models.IntegerField(blank=True, null=True)
    order_id = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.user.email
    


class ConsultationGuest(models.Model):
    consultation = models.CharField(max_length=10000, null=False, blank=False)
    details = models.CharField(max_length=10000, null=False, blank=False)
    fee_in_naira = models.IntegerField(blank=True, null=True)
    fee_in_dollars = models.IntegerField(blank=True, null=True)
    order_id = models.CharField(max_length=10, null=True, blank=True)
    

    def __str__(self):
        return self.consultation