# Generated by Django 4.0.3 on 2022-05-23 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elder', '0007_alter_vital_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField()),
                ('message', models.TextField()),
                ('approved', models.BooleanField(default=False)),
                ('approved_at', models.DateTimeField()),
                ('patid', models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.CASCADE, to='elder.patientrelative')),
                ('staffid', models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.CASCADE, to='elder.medicalstaff')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
    ]
