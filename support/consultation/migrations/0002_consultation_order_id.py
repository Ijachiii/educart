# Generated by Django 4.1.7 on 2023-08-28 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("consultation", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="consultation",
            name="order_id",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
