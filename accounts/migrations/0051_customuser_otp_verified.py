# Generated by Django 4.1.7 on 2023-09-10 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0050_customuser_free_consultation"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="otp_verified",
            field=models.BooleanField(default=False),
        ),
    ]
