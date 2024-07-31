from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class Usermodel(UserAdmin):
    list_display=['username','user_type']
admin.site.register(doctor)
admin.site.register(Patient)
admin.site.register(CustomUser,Usermodel)
admin.site.register(Visit)
admin.site.register(Reminder)
admin.site.register(Inquiry)
admin.site.register(Medicine)
