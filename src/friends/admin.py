from django.contrib import admin

from .models import FriendRequest, FriendList, Catsitter

# Register your models here.
admin.site.register(FriendList)
admin.site.register(FriendRequest)
admin.site.register(Catsitter)
