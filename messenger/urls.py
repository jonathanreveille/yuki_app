from django.urls import path

from . import views
from .views import MessengerCreateReplyView, MessengerDeleteView, MessengerListView, MessengerCreateView, MessengerDetailView

app_name = "messenger"

urlpatterns = [
    path('message_list/', MessengerListView.as_view(), name='message_list'),
    path('message_create/', MessengerCreateView.as_view(), name='message_create'),
    path('message_delete/<int:pk>', MessengerDeleteView.as_view(), name='message_delete'),
    path('message_detail/<int:pk>', MessengerDetailView.as_view(), name='message_detail'),
    path('message_reply/<int:pk>', MessengerCreateReplyView.as_view(), name='message_reply'),
]
