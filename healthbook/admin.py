from django.contrib import admin

from .models import HealthBook, Medication

# Register your models here.
admin.site.register(HealthBook)
admin.site.register(Medication)