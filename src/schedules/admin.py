from django.contrib import admin

from .models import Task, Schedule, TimeOfDay


admin.site.register(Task)
admin.site.register(Schedule)
admin.site.register(TimeOfDay)
