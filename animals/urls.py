from django.urls import path
from . import views

app_name = "animals"

urlpatterns = [
    path('', views.home, name='home'),
    path('create_pet/', views.create_pet, name='create_pet'),
    path('see_pet/', views.see_pet, name='see_pet'),
    ]