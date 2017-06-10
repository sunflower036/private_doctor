from django.contrib import admin

# Register your models here.
from private_doctor import models
admin.site.register(models.Doctor)