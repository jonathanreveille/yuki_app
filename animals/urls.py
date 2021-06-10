from django.urls import path
from . import views
from .views import PetDeleteView, PetUpdateView

app_name = "animals"

urlpatterns = [
    path('', views.home, name='home'),
    path('create_pet/', views.create_pet, name='create_pet'),
    path('see_pet/', views.see_pet, name='see_pet'),
    path('update_pet/<int:pk>', PetUpdateView.as_view(), name='update_pet'),
    path('delete_pet/<int:pk>', PetDeleteView.as_view(), name='delete_pet'),
    ]