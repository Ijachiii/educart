# Generated by Django 4.1.7 on 2023-09-26 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0053_alter_consultant_price_per_hour_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="OrderHistoryGuest",
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
                ("order_id", models.CharField(max_length=50)),
                ("order_type", models.CharField(max_length=50)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=20)),
                ("date", models.DateTimeField()),
                ("status", models.CharField(max_length=50)),
            ],
        ),
    ]
