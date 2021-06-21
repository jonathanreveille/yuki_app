from django.urls import path
from . import views
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete
from .views import  SchedulePetList, SchedulePetCreate, ScheduleDetailView, ScheduleDeleteView

app_name = "schedules"

urlpatterns = [

    #task part
    path('', TaskList.as_view(), name='task_list'),
    path('task/<int:pk>', TaskDetail.as_view(), name='task'),
    path('task_create/', TaskCreate.as_view(), name='task_create'),
    path('task_update/<int:pk>', TaskUpdate.as_view(), name='task_update'),
    path('task_delete/<int:pk>', TaskDelete.as_view(), name='task_delete'),

    #schedule part
    path('schedule_list/', SchedulePetList.as_view(), name="schedule_list"),
    path('schedule_create/', SchedulePetCreate.as_view(), name="schedule_create"),
    path('schedule/<int:pk>', ScheduleDetailView.as_view(), name='schedule_detail'),
    path('schedule_delete/<int:pk>', ScheduleDeleteView.as_view(), name='schedule_delete'),
    path('schedule_search/', views.schedule_search, name="schedule_search"),

    # path('see_pet_schedule/', views.see_pet_schedule, name='see_pet_schedule'),
]
