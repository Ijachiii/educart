# Generated by Django 4.1.7 on 2023-09-24 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sevis", "0017_alter_sevisinformationuser_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="sevisinformationuser",
            name="payment_status",
            field=models.CharField(
                blank=True, default="Payment Pending", max_length=100, null=True
            ),
        ),
    ]
