# Generated by Django 4.1.7 on 2023-07-18 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="sevisinformation",
            name="international_passport",
            field=models.FileField(
                default="/views.py", upload_to="international_passport/"
            ),
        ),
        migrations.AddField(
            model_name="sevisinformation",
            name="last_name",
            field=models.CharField(default="AUdu", max_length=100),
            preserve_default=False,
        ),
    ]
