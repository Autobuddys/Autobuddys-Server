from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

# ---------------------------
# Custom User Manager
# ---------------------------
class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, phone, is_medical, password=None):
        if not email:
            raise ValueError("User must have an email address")
        if not phone:
            raise ValueError("User must have a phone number")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, phone=phone, is_medical=is_medical)
        user.is_active = True  # Set active regardless of is_medical
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password, phone):
        user = self.create_user(email, name, phone, True, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

# ---------------------------
# Custom User Model
# ---------------------------
class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, unique=True)
    is_medical = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']

    def get_full_name(self):
        return self.name

    def get_mobile(self):
        return self.phone

    def __str__(self):
        return f"{self.id} - {self.email} - {self.name}"

# ---------------------------
# Medical Staff Profile
# ---------------------------
class MedicalStaff(models.Model):
    medstaff = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    hospname = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.hospname} City {self.city}"

# ---------------------------
# Patient Relative Information
# ---------------------------
class PatientRelative(models.Model):
    patrel = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    pname = models.CharField(max_length=100)
    pphone = models.CharField(max_length=15)
    page = models.IntegerField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=20)
    dname = models.CharField(max_length=255)
    dphone = models.CharField(max_length=15)

    class Meta:
        ordering = ['pname']

    def __str__(self):
        return self.pname

# ---------------------------
# Vitals Monitoring
# ---------------------------
class Vital(models.Model):
    patid = models.ForeignKey(PatientRelative, on_delete=models.CASCADE)
    tempval = models.FloatField()
    spo2val = models.FloatField()
    bpmval = models.FloatField()
    bpval = models.FloatField(default=23)
    entered_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['entered_at']

    def __str__(self):
        return f"{self.entered_at} - {self.patid}"

# ---------------------------
# Notifications
# ---------------------------
class Notification(models.Model):
    patid = models.ForeignKey(PatientRelative, on_delete=models.CASCADE)
    staffid = models.ForeignKey(MedicalStaff, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    message = models.TextField()
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    removefromlist = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Patient ID {self.patid} - Staff ID {self.staffid}"

# ---------------------------
# Image Encoding Store (Face Embeddings)
# ---------------------------
class ImageStore(models.Model):
    patid = models.ForeignKey(PatientRelative, on_delete=models.CASCADE)
    pname = models.CharField(max_length=100)
    encoding = ArrayField(models.FloatField())  # PostgreSQL only

    def __str__(self):
        return f"Patient ID {self.patid} - pname {self.pname}"

# ---------------------------
# Patient Image Upload
# ---------------------------
class PatientImage(models.Model):
    patid = models.IntegerField(unique=True, primary_key=True)
    imageFile = models.FileField(upload_to='media/')

    def __str__(self):
        return f"Patient ID {self.patid}"

