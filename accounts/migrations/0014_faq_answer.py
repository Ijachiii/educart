# Generated by Django 4.1.7 on 2023-07-28 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0013_rename_faqs_faq_rename_userfaqs_userfaq"),
    ]

    operations = [
        migrations.AddField(
            model_name="faq",
            name="answer",
            field=models.CharField(default="ijachi", max_length=10000),
            preserve_default=False,
        ),
    ]
