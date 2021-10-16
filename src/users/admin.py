from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from .models import User
from .forms import UserChangeForm, UserCreationForm

class UserAdmin(AuthUserAdmin):
    """admin interface to add users or change users"""
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('username', 'email', 'first_name', 'is_staff', 'location', 'role')


# Register your models here.
admin.site.register(User, UserAdmin)