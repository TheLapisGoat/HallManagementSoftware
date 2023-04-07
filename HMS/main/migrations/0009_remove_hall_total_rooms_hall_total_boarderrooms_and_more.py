# Generated by Django 4.1.7 on 2023-04-07 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0008_merge_20230406_1824"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="hall",
            name="total_rooms",
        ),
        migrations.AddField(
            model_name="hall",
            name="total_boarderrooms",
            field=models.IntegerField(default=0, verbose_name="Total Boarder Rooms"),
        ),
        migrations.AlterField(
            model_name="student",
            name="rollNumber",
            field=models.CharField(
                max_length=100, unique=True, verbose_name="Roll Number"
            ),
        ),
    ]