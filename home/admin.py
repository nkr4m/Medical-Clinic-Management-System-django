from django.contrib import admin

# Register your models here.


from .models import *


admin.site.register(Patient)
admin.site.register(Treatment)
admin.site.register(Tag)
admin.site.register(Appoinment)