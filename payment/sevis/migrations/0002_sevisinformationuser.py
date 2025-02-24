# Generated by Django 4.1.7 on 2023-08-24 09:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("sevis", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SevisInformationUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("sevis_id", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("given_name", models.CharField(max_length=100)),
                ("date_of_birth", models.DateField(blank=True, null=True)),
                ("form", models.FileField(upload_to="form/")),
                ("passport", models.ImageField(upload_to="passport/")),
                (
                    "international_passport",
                    models.FileField(upload_to="international_passport/"),
                ),
                ("form_type", models.CharField(max_length=100)),
                (
                    "category",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("au pair ($35)", "Au Pair ($35)"),
                            ("camp counselor ($35)", "Camp Counselor ($35)"),
                            ("summer work/travel ($35)", "Summer Work/Travel ($35)"),
                            ("others ($200)", "Others ($200)"),
                        ],
                        max_length=100,
                        null=True,
                    ),
                ),
                ("email", models.CharField(max_length=100)),
                ("country_of_citizenship", models.CharField(max_length=100)),
                ("country_of_birth", models.CharField(max_length=100)),
                ("phone_number", models.CharField(max_length=15)),
                ("street_address_1", models.CharField(max_length=200)),
                ("street_address_2", models.CharField(max_length=200)),
                ("country", models.CharField(max_length=200)),
                ("state", models.CharField(max_length=200)),
                ("city", models.CharField(max_length=200)),
                (
                    "fee_in_dollars",
                    models.CharField(blank=True, max_length=10, null=True),
                ),
                (
                    "fee_in_naira",
                    models.CharField(blank=True, max_length=10, null=True),
                ),
                ("order_id", models.CharField(blank=True, max_length=10, null=True)),
                ("order_fee", models.CharField(blank=True, max_length=10, null=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sevis_information",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
