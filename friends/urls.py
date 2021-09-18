from django.urls import path

from . import views
from .views import CatsitterCreateView, CatsitterList, FriendRequestDeleteView, FriendRequestListView, FriendListView, FriendRequestDetailView

app_name = "friends"

urlpatterns = [
    # Search for user
    path('search_for_friends/', views.search_for_friends, name='search_for_friends'),
    path('search_friends_result/', views.search_friends_result, name='search_friends_result'),

    # Friend requests
    path('send_friend_request/<int:pk>', views.send_friend_request, name="send_friend_request"),
    path('accept_friend_request/', views.accept_friend_request, name="accept_friend_request"),
    path('see_friend_request_list/', FriendRequestListView.as_view(), name="see_friend_request_list"),
    path('decline_friend_request/<int:pk>', FriendRequestDeleteView.as_view(), name="decline_friend_request"),

    path('see_friend_request_detail/<int:pk>',FriendRequestDetailView.as_view(), name="see_friend_request_detail"), #new line for notifications

    #User's friends
    path('see_friends/', FriendListView.as_view(), name='see_friends'),
    #new try
    path('delete_mutual_friend/', views.delete_friend, name="delete_mutual_friend"),


    # Catsitter
    path('catsitter_list/', CatsitterList.as_view(), name='catsitter_list'),
    path('catsitter_create/', CatsitterCreateView.as_view(), name='catsitter_create'),
    path('catsitter_delete/', views.delete_catsitter_request, name="delete_catsitter_request"),
    path('catsitter_get_cat_info/<int:pk>', views.catsitter_get_cat_info, name="catsitter_get_cat_info")
]
