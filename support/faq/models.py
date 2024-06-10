from django.db import models

# Create your models here.
class Faq(models.Model):
    CATEGORY_CHOICES = (
        ("payment", "Payment"),
        ("account", "Account"),
        ("security", "Security")
    )

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    question = models.CharField(max_length=256)
    answer = models.TextField()

    def __str__(self):
        return self.question