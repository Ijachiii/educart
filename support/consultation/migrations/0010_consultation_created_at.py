# Generated by Django 4.1.7 on 2023-09-05 11:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("consultation", "0009_alter_consultation_consultant"),
    ]

    operations = [
        migrations.AddField(
            model_name="consultation",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                default=datetime.datetime(
                    2023, 9, 5, 11, 32, 17, 156161, tzinfo=datetime.timezone.utc
                ),
            ),
            preserve_default=False,
        ),
    ]
