# Generated by Django 4.1.7 on 2023-07-19 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_sevisinformation_i_20_phone_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sevisinformation",
            name="I_20_phone_number",
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name="sevisinformation",
            name="international_passport",
            field=models.FileField(upload_to="international_passport/"),
        ),
    ]
