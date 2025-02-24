# Generated by Django 4.1.7 on 2023-09-05 10:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0048_remove_consultant_location_consultant_bio_and_more"),
        ("consultation", "0008_consultation_consultant"),
    ]

    operations = [
        migrations.AlterField(
            model_name="consultation",
            name="consultant",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="consultant",
                to="accounts.consultant",
            ),
        ),
    ]
