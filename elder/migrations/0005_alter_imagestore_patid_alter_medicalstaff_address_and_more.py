# elder/migrations/0005_alter_imagestore_patid_alter_medicalstaff_address_and_more.py
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models
import django.contrib.postgres.fields

def move_encoding_to_json(apps, schema_editor):
    ImageStore = apps.get_model('elder', 'ImageStore')
    for image in ImageStore.objects.all():
        if image.encoding is not None:
            image.encoding_json = image.encoding
            image.save()
        else:
            image.encoding_json = []
            image.save()

def move_encoding_back(apps, schema_editor):
    ImageStore = apps.get_model('elder', 'ImageStore')
    for image in ImageStore.objects.all():
        image.encoding = image.encoding_json
        image.save()

class Migration(migrations.Migration):

    dependencies = [
        ('elder', '0004_alter_imagestore_encoding_alter_imagestore_patid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagestore',
            name='encoding_json',
            field=models.JSONField(null=True, blank=True),
        ),
        migrations.RunPython(move_encoding_to_json, reverse_code=move_encoding_back),
        migrations.RemoveField(
            model_name='imagestore',
            name='encoding',
        ),
        migrations.RenameField(
            model_name='imagestore',
            old_name='encoding_json',
            new_name='encoding',
        ),
        migrations.AlterField(
            model_name='imagestore',
            name='patid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elder.patientrelative'),
        ),
        migrations.AlterField(
            model_name='medicalstaff',
            name='address',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='medicalstaff',
            name='city',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='medicalstaff',
            name='hospname',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='medicalstaff',
            name='medstaff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='medicalstaff',
            name='pincode',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='medicalstaff',
            name='state',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='notification',
            name='approved_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='notification',
            name='patid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elder.patientrelative'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='staffid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elder.medicalstaff'),
        ),
        migrations.AlterField(
            model_name='patientimage',
            name='patid',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='elder.patientrelative'),
        ),
        migrations.AlterField(
            model_name='patientrelative',
            name='address',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='patientrelative',
            name='city',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='patientrelative',
            name='dname',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='patientrelative',
            name='dphone',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='patientrelative',
            name='patrel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='patientrelative',
            name='pincode',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='patientrelative',
            name='pphone',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='patientrelative',
            name='state',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(max_length=15, unique=True),
        ),
        migrations.AlterField(
            model_name='vital',
            name='entered_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='vital',
            name='patid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elder.patientrelative'),
        ),
    ]