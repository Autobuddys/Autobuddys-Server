from datetime import datetime
from http.cookiejar import DefaultCookiePolicy
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.postgres.fields import ArrayField
from matplotlib.pyplot import axes
# Create your models here.

class UserProfileManager(BaseUserManager):
    def create_user(self, email, name,phone, is_medical,password=None):
        if not email:
            raise ValueError("User must have an email address")
        if not phone:
            raise ValueError("User must have a phone number")
        email = self.normalize_email(email)
        user = self.model(email=email,name=name,phone=phone,is_medical=is_medical)
        # print("I am in UserProfileManager : ",user.is_medical)
        if is_medical==True:user.is_active = False
        else:user.is_active=True
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,email,name,password,phone,):
        user=self.create_user(email,name,phone,True,password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using = self._db)

        return user

class UserProfile(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=255,unique=True)
    name = models.CharField(max_length=255)
    phone = models.TextField(max_length=10,unique=True)
    is_medical = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','phone']

    def get_full_name(self):
        return self.name
    
    def get_mobile(self):
        return self.phone
    
    def __str__(self):
        return (str(self.id)+" - "+self.email)


class MedicalStaff(models.Model):
    medstaff = models.ForeignKey(UserProfile,on_delete=models.CASCADE,unique=True,primary_key=False)
    hospname = models.TextField()
    address = models.TextField()
    city = models.TextField()
    state = models.TextField()
    pincode = models.IntegerField()


    def __str__(self):
        return(str(self.id))


class PatientRelative(models.Model):
    #your relation to the patient?
    patrel = models.ForeignKey(UserProfile,on_delete=models.CASCADE,db_index=False)
    pname = models.CharField(max_length=100)
    pphone = models.CharField(max_length=10)
    page = models.IntegerField()
    address = models.TextField()
    city = models.TextField()
    state = models.TextField()
    pincode = models.IntegerField()
    dname = models.TextField()
    dphone = models.CharField(max_length=10)

    class Meta:
        ordering=['pname']


    def __str__(self):
        return(str(self.id))

class Vital(models.Model):
    patid = models.ForeignKey(PatientRelative,on_delete=models.CASCADE,db_index=False)
    tempval = models.FloatField()
    spo2val = models.FloatField()
    bpmval = models.FloatField()
    bpval = models.FloatField(default=23)
    entered_at = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ['entered_at']

    def __str__(self):
        return(str(self.entered_at)+" - "+str(self.patid))

class Notification(models.Model):
    patid = models.ForeignKey(PatientRelative,on_delete=models.CASCADE,db_index=False)
    staffid = models.ForeignKey(MedicalStaff,on_delete=models.CASCADE,db_index=False)
    created_at = models.DateTimeField(default=datetime.now)
    message = models.TextField()
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    removefromlist = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return("Patient ID "+str(self.patid)+" - "+"Staff ID "+str(self.staffid))

class ImageStore(models.Model):
    patid = models.ForeignKey(PatientRelative,on_delete=models.CASCADE,db_index=False)
    pname=models.CharField(max_length=100)
    encoding=ArrayField(models.FloatField())

    def __str__(self):
        return("Patient ID "+str(self.patid)+" - "+"pname "+str(self.pname))


class PatientImage(models.Model):
    patid = models.IntegerField(unique=True,primary_key=True)
    imageFile=models.FileField(upload_to='media/')

    def __str__(self):
        return("Patient ID "+str(self.patid))



