from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    # ex : /register/create_account/
    # path('search/', views.search, name="search"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
]