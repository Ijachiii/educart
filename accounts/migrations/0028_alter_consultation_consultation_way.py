# Generated by Django 4.1.7 on 2023-08-01 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0027_consultation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="consultation",
            name="consultation_way",
            field=models.CharField(
                choices=[
                    ("zoom video call", "Zoom Video Call"),
                    ("phone call", "Phone Call"),
                ],
                max_length=20,
            ),
        ),
    ]
