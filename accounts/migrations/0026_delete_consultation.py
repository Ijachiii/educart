# Generated by Django 4.1.7 on 2023-08-01 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0025_consultation_fee_in_dollars_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Consultation",
        ),
    ]
