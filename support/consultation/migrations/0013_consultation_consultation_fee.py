# Generated by Django 4.1.7 on 2023-09-20 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("consultation", "0012_remove_consultation_consultation_fee"),
    ]

    operations = [
        migrations.AddField(
            model_name="consultation",
            name="consultation_fee",
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
