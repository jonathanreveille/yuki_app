from django.http.response import HttpResponse
from friends.models import FriendRequest
from notifications.models import Notification
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views import View

from .models import Pet
from .forms import PetCreationForm
from friends.forms import SearchForFriendForm
from users.models import User
from friends.models import FriendRequest #new line
from messenger.models import Messenger
# from friends.forms import SearchForFriendForm


# Create your views here.
def home(request):
    """view method to see homepage"""
    # form = SearchForFriendForm()
    return render(request, 'animals/home.html')

@login_required
def create_pet(request):
    """method to create animals
    from the user"""

    if request.method == "POST":
        form = PetCreationForm(request.POST)

        if form.is_valid():
            owner = request.user
            name = form.cleaned_data.get("name")
            weight = form.cleaned_data.get("weight")
            age = form.cleaned_data.get("age")
            specie = form.cleaned_data.get("specie")

            Pet.objects.get_or_create(
                name=name,
                weight=weight,
                age=age,
                specie=specie,
                owner=owner,
            )

        return redirect('animals:home')

    else:

        form = PetCreationForm()

    return render(request, 'animals/pet_form.html', {'form':form})

@login_required
def see_pet(request):
    """view to allow the user
    to see his pets"""
    user = request.user
    user_pets = Pet.objects.filter(owner=user)

    context = {
        'user_pets' : user_pets,
    }

    return render(request, 'animals/see_pet.html', context)


class PetUpdateView(LoginRequiredMixin, UpdateView):
    """update a pet"""

    model = Pet
    fields = ('name','age','weight','avatar')
    success_url = reverse_lazy('animals:see_pet')

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         name = form.cleaned_data.get("name")
    #         age = form.cleaned_data.get("age")
    #         weight = form.cleaned_data.get("weight")
    #         avatar = form.cleaned_data.get("avatar")

    #         updated_cat = Pet.objects.get(
    #                         owner=request.user,
    #                         name=name,
    #                         age=age,
    #                         weight=weight,
    #                         avatar=avatar)

    #     return updated_cat

class PetDeleteView(LoginRequiredMixin, DeleteView):
    """delete a pet"""

    model = Pet
    content_object_name = 'pet'
    template_name = 'animals/pet_confirm_delete.html'
    success_url = reverse_lazy('animals:see_pet')


######################################################
################## NOTIFICATIONS #####################
######################################################

class FriendRequestNotification(View):
    def get(self, request, notification_pk, friend_request_pk, *args, **kwargs):
        """ grab the notification object, and grab if it's a message
        or a friend request with object_pk"""
        notification = Notification.objects.get(pk=notification_pk)
        friend_request = FriendRequest.objects.get(pk=friend_request_pk)
        notification.user_has_seen = True
        notification.save()

        #return render(request, 'friends/friend_request_detail.html')
        return redirect('friends:see_friend_request_detail', pk=friend_request.id)
        # see_friend_request_detail


class MessageNotification(View):
    def get(self, request, notification_pk, message_pk, *args, **kwargs):
        """ grab the notification object, and grab if it's a message
        or a friend request with object_pk"""

        notification = Notification.objects.get(pk=notification_pk)
        message = Messenger.objects.get(pk=message_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('messenger:message_detail', pk=message.id)


class RemoveNotification(View):
    def delete(self, request, notification_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        notification.user_has_seen = True
        notification.save()

        return HttpResponse('Success', content_type="text/plain")
