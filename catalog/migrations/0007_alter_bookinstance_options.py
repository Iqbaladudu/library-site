# Generated by Django 4.2.4 on 2023-08-06 04:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0006_bookinstance_borrower"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="bookinstance",
            options={
                "ordering": ["due_back"],
                "permissions": (("can_mark_returned", "Set book as returned"),),
            },
        ),
    ]
