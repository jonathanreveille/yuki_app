from django.urls import path

from .views import (HealthBookCreateView,
                    HealthBookListView,
                    HealthBookUpdateView,
                    MedicationDeleteView,
                    MedicationListView,
                    MedicationCreateView,
                    MedicationUpdateView)


app_name = "healthbook"

urlpatterns = [
    # HeathBook
    path('healthbook_list/',
         HealthBookListView.as_view(),
         name="healthbook_list"),
    path('healthbook_create/',
         HealthBookCreateView.as_view(),
         name="healthbook_create"),
    path('healthbook_update/<int:pk>',
         HealthBookUpdateView.as_view(),
         name="healthbook_update"),
    # Medication
    path('medication_list/',
         MedicationListView.as_view(),
         name="medication_list"),
    path('medication_create/',
         MedicationCreateView.as_view(),
         name="medication_create"),
    path('medication_update/<int:pk>',
         MedicationUpdateView.as_view(),
         name="medication_update"),
    path('medication_delete/<int:pk>',
         MedicationDeleteView.as_view(),
         name="medication_delete"),
]
