# Generated by Django 4.1.7 on 2023-08-15 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0036_alter_customuser_country_of_residence"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="addressbook",
            name="apartment_number",
        ),
        migrations.AddField(
            model_name="addressbook",
            name="state",
            field=models.CharField(default="Lagos", max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="addressbook",
            name="zip_code",
            field=models.CharField(default="100276", max_length=12),
            preserve_default=False,
        ),
    ]
