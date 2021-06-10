from django.urls import path
from .views import HealthBookList, HealthBookCreate

app_name = "healthbook"

urlpatterns = [
    path('healthbook_list/', HealthBookList.as_view(), name="healthbook_list"),
    path('healthbook_create/', HealthBookCreate.as_view(), name="healthbook_create"),
]