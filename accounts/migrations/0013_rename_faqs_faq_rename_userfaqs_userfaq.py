# Generated by Django 4.1.7 on 2023-07-26 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0012_userfaqs"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="FAQs",
            new_name="Faq",
        ),
        migrations.RenameModel(
            old_name="UserFAQs",
            new_name="UserFaq",
        ),
    ]
