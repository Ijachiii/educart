# Generated by Django 4.1.7 on 2023-09-21 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sevis", "0009_sevisinformationguest_charges_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sevisinformationguest",
            name="fee_in_dollars",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="sevisinformationguest",
            name="fee_in_naira",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
