# Generated by Django 4.0.3 on 2022-06-03 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elder', '0011_notification_rejected'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='removefromlist',
            field=models.BooleanField(default=False),
        ),
    ]
