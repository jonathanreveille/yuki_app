from notifications.models import Notification
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

from .forms import SearchForFriendForm
from users.models import User
from .models import  FriendRequest, FriendList
from notifications.models import Notification


@login_required
def search_for_friends(request):
    """method to search through the
    users inside the application"""

    form = SearchForFriendForm()

    return render(request, 'friends/search_friends.html', {'form':form})


@login_required
def search_friends_result(request):
    """view to see the results of from the
    user's query"""

    # AMELIORER CETTE METHODE POUR VOIR QUE LES PERSONNES QUI
    # NE SONT PAS ENCORE DANS NOTRE LISTE d'AMI

    context = {}

    if request.method == "GET":
        form = SearchForFriendForm(request.GET)

        if form.is_valid():
            user_search = form.cleaned_data.get('query_friend_search')
            users_found = User.objects.filter(username__icontains=user_search)

            context = {
                'user_search' : user_search,
                'users_found': users_found, 
            }

        return render(request, 'friends/search_friends_result.html', context)

    else:
        
        form = SearchForFriendForm()

    return render(request, 'friends/search_friends.html', {'form':form})


@login_required
def send_friend_request(request, pk):
    """view that allows the user to click 
    on send request link to add send a friend
    request"""

    sender = request.user
    receiver = User.objects.get(id=pk)

    friend_request, created = FriendRequest.objects.get_or_create(
        sender=sender,
        receiver=receiver,
        )

    if created:
        friend_request.save()
        notification = Notification.objects.create(notification_type=1, from_user=request.user, to_user=receiver, friend_request=friend_request)
    
    return render(request, 'animals/home.html')


class FriendRequestDetailView(LoginRequiredMixin, DetailView):
    """view to see the unique friend request"""

    model = FriendRequest
    context_object_name = 'friend_request'
    template_name = 'friends/friend_request_detail.html'
 

class FriendRequestListView(LoginRequiredMixin, ListView):
    """list to see all pending friends requests"""

    models = FriendRequest
    context_object_name = 'friend_requests'
    template_name = 'friends/friend_request_list.html'

    def get_context_data(self, **kwargs):
        """equivalent to context dict to use variables"""
        
        context = super().get_context_data(**kwargs)
        context["friend_requests"] = FriendRequest.objects.filter(
            receiver__username=self.request.user,
            is_active=True
            )
        return context

    def get_queryset(self):
        """Returns the list of items for this view.
        If a user clicks on the message, we update
        the field is_read of Messenger model"""

        friend_request = FriendRequest.objects.filter(receiver=self.request.user)
        return friend_request


@login_required
def accept_friend_request(request):
    """view to accept a friend request,  only
    friend request with  is_active = True are shown
    to the user"""

    if request.method == "POST":
        sender_id = request.POST['from_user']
        receiver_id = request.POST['to_user']

        sender = User.objects.get(id=sender_id)
        receiver = User.objects.get(id=receiver_id)

        friends = FriendList.objects.get_or_create(
            user = receiver,
            friend = sender,
        )

        FriendList.objects.get_or_create(
            user = sender,
            friend = receiver,
        )

        context = {
            'friends' : friends
        }

        friend_added = FriendRequest.objects.filter(receiver=request.user,
                                                    sender=sender_id)
        friend_added.update(is_active=False)

        messages.success(request, "You accepted your last friend requests")

    return render(request, 'animals/home.html', context)


class FriendListView(LoginRequiredMixin, ListView):

    model = FriendList
    context_object_name = 'friends'
    template_name = 'friends/see_friend_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["friends"] = context["friends"].filter(user=self.request.user)
        return context


@login_required
def delete_friend(request):
    """view to delete a friend"""

    if request.method == "POST":
        user =  request.POST['user']
        friend = request.POST['to_delete_user']

        #delete the friend request so user can add each other again
        fr = FriendRequest.objects.filter(sender=user, receiver=friend) 
        fr.delete()

        #delete the relationship for each user
        fl = FriendList.objects.filter(user=user, friend=friend) #delete for user
        fl_friend = FriendList.objects.filter(user=friend, friend=user) #delete for friend
        fl.delete()
        fl_friend.delete()

        messages.success(request, "You have deleted your friend")

        return redirect('animals:home')

    else:

        friends = FriendList.objects.filter(user=request.user).all()
        context = {
            'friends': friends,
        }

    return render(request, 'friends/friend_delete.html', context)









# class FriendListDelete(LoginRequiredMixin, DeleteView):
#     """view to unfriend a friend in the
#     user list of friends"""
    
#     model = FriendList
#     context_object_name = 'friend'
#     template_name = 'friends/friend_confirm_delete.html'
    
#     def post(self,request, pk):
#         fl = FriendList.objects.filter(id=pk)
#         friend = fl.filter(friend=request.user.friend.id)
#         relationship = FriendList.objects.filter(username__icontains=request.user,
#                                                 friend = friend)
#         relationship.delete()
#         return reverse_lazy('friends:see_friends')



#####################################################################
#     if request.method == "POST":
#         sender_id = request.POST['from_user']
#         receiver_id = request.POST['to_user']

#         sender = User.objects.get(id=sender_id)
#         receiver = User.objects.get(id=receiver_id)

#         friends = FriendList.objects.get_or_create(
#             user = receiver,
#             friend = sender,
#         )

#         FriendList.objects.get_or_create(
#             user = sender,
#             friend = receiver,
#         )

#         context = {
#             'friends' : friends
#         }

#         friend_added = FriendRequest.objects.filter(receiver=request.user,
#                                                     sender=sender_id)
#         friend_added.update(is_active=False)

#         messages.success(request, "You accepted your last friend requests")

#     return render(request, 'animals/home.html', context)



    # def post(self, request, pk, *args, **kwargs):
    #     friend_list = FriendList.objects.filter(pk=pk)
    #     user_profile = get_object_or_404(FriendList, id=request.user.id)
    #     friend_profile = friend_list.friend
    #     user_profile.friend.remove(friend_list.friend) # A removes B
    #     friend_profile.friend.remove(user_profile) # B removes A
    #     return reverse_lazy('friends:see_friends')


        # relation = FriendList.objects.filter(id=pk)
        # user_profile = relation.user 
        # friend_profile = relation.friend
        # user_profile.remove(friend_profile)
        # friend_profile.remove(user_profile)
        # return 


        # self.user_profile = request.user
        # self.friend_profile = User.objects.get(pk=pk) # Profile instance has the same id as user
        # self.user_profile.friends.remove(self.friend_profile) # A removes B
        # self.friend_profile.friends.remove(self.user_profile) # B removes A
        

    # def delete(self, request, *args, **kwargs):
    #     """
    #     Call the delete() method on the fetched object and then redirect to the
    #     success URL.
    #     """

    #     self.object = self.get_object()
    #     success_url = self.get_success_url()
    #     self.object.delete()
    #     return HttpResponseRedirect(success_url)

# def delete_friend(request, pk):
#     """method to delete a friend for the user
#     and for the friend"""

#     user_profile = request.user
#     friend_profile = User.objects.get(pk=pk) # Profile instance has the same id as user
#     user_profile.friends.remove(friend_profile) # A removes B
#     friend_profile.friends.remove(user_profile) # B removes A
#     return reverse_lazy('friends:see_friends')



#     def get_queryset(self, friend_id):
#         user_profile = self.request.user
#         friend_profile = get_object_or_404(User, pk=friend_id)
#         user_profile.friends.remove(friend_profile)
#         friend_profile.friends.remove(user_profile)
