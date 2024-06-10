# Generated by Django 4.1.7 on 2023-09-22 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sevis", "0012_sevisinformationguest_rate"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="sevisinformationguest",
            name="country",
        ),
        migrations.RemoveField(
            model_name="sevisinformationguest",
            name="passport",
        ),
        migrations.AlterField(
            model_name="sevisinformationguest",
            name="city",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="sevisinformationguest",
            name="last_name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="sevisinformationguest",
            name="state",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="sevisinformationguest",
            name="street_address_1",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
