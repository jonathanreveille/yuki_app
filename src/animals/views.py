from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views import View
from django.db import transaction

from .models import Pet
from .forms import PetCreationForm, PetEditForm, PetUpdateForm
from friends.models import FriendRequest
from messenger.models import Messenger
from notifications.models import Notification


# Create your views here.
def home(request):
    """view method to see homepage"""
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

    return render(request, 'animals/pet_create_form.html', {'form': form})


@login_required
def see_pet(request):
    """view to allow the user
    to see his pets"""
    user = request.user
    user_pets = Pet.objects.filter(owner=user)

    context = {
        'user_pets': user_pets,
    }
    return render(request, 'animals/see_pet.html', context)


class PetUpdateView(LoginRequiredMixin, UpdateView):
    """update a pet"""
    model = Pet
    success_url = reverse_lazy('animals:see_pet')
    form_class = PetUpdateForm

    def get_queryset(self):
        qs = super().get_queryset()
        qs.filter(owner=self.request.user)
        return qs


class PetDeleteView(LoginRequiredMixin, DeleteView):
    """delete a pet"""
    model = Pet
    content_object_name = 'pet'
    template_name = 'animals/pet_confirm_delete.html'
    success_url = reverse_lazy('animals:see_pet')


@login_required
@transaction.atomic
def change_pet_avatar(request, pk):
    """method to change the pet's profile picture"""

    if request.method == "POST":
        form = PetEditForm(request.POST, request.FILES)

        if form.is_valid():
            avatar = form.cleaned_data.get("avatar")

            to_update = Pet.objects.get(pk=pk)
            to_update.avatar = avatar
            to_update.save()

        return redirect('animals:see_pet')

    else:
        form = PetEditForm()
        pet = Pet.objects.get(pk=pk)
        context = {
            'form': form,
            'pet': pet,
        }

    return render(request, 'animals/change_pet_avatar.html', context)


# Notifications
class FriendRequestNotification(View):
    def get(self, request, notification_pk,
            friend_request_pk, *args, **kwargs):
        """ grab the notification object, and grab if it's a message
        or a friend request with object_pk"""
        notification = Notification.objects.get(pk=notification_pk)
        friend_request = FriendRequest.objects.get(pk=friend_request_pk)
        notification.user_has_seen = True
        notification.save()

        return redirect('friends:see_friend_request_detail',
                        pk=friend_request.id)


class MessageNotification(View):
    def get(self, request, notification_pk,
            message_pk, *args, **kwargs):
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
