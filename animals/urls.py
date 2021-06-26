from django.urls import path
from . import views
from .views import PetDeleteView, PetUpdateView, FriendRequestNotification, MessageNotification, RemoveNotification

app_name = "animals"

urlpatterns = [
    path('', views.home, name='home'),
    path('create_pet/', views.create_pet, name='create_pet'),
    path('see_pet/', views.see_pet, name='see_pet'),
    path('update_pet/<int:pk>', PetUpdateView.as_view(), name='update_pet'),
    path('delete_pet/<int:pk>', PetDeleteView.as_view(), name='delete_pet'),
    path('notification/<int:notification_pk>/friends/see_friend_request_list/<int:friend_request_pk>', FriendRequestNotification.as_view(),name='friend_request_notification'),
    path('notification/<int:notification_pk>/messenger/message_detail/<int:message_pk>', MessageNotification.as_view(),name='message_notification'),
    path('notification/delete/<int:notification_pk>', RemoveNotification.as_view(), name="notification-delete"),
]