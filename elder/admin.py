from django.contrib import admin
from elder.models import UserProfile,MedicalStaff,PatientRelative, Vital, Notification,ImageStore

admin.site.register(UserProfile)
admin.site.register(MedicalStaff)
admin.site.register(PatientRelative)
admin.site.register(Vital)
admin.site.register(Notification)
admin.site.register(ImageStore)
# admin.site.register(PostImage)
# Register your models here.
