# Generated by Django 4.1.7 on 2023-04-08 11:46

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_hallemployee_alter_person_role_hallemployeeleave_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="telephoneNumber",
            field=phonenumber_field.modelfields.PhoneNumberField(
                max_length=128, region=None, verbose_name="Telephone Number"
            ),
        ),
    ]
