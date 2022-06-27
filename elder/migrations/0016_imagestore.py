# Generated by Django 4.0.3 on 2022-06-22 07:11

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elder', '0015_delete_postimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageStore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pname', models.CharField(max_length=100)),
                ('encoding', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), size=None)),
                ('patid', models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.CASCADE, to='elder.patientrelative')),
            ],
        ),
    ]
