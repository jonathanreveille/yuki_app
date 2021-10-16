from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from .forms import SearchForFriendForm, CreateCatsitterForm
from .models import  Catsitter, FriendRequest, FriendList
from animals.models import Pet
from users.models import User
from notifications.models import Notification
from healthbook.models import HealthBook
from schedules.models import Schedule


@login_required
def search_for_friends(request):
    """method to search through the
    users inside the application"""

    form = SearchForFriendForm()

    context = {
        'form' : form,
        }

    return render(request, 'friends/search_friends_result.html', context)


@login_required
def search_friends_result(request):
    """view to see the results of from the
    user's query"""

    if request.method == "GET":
        form = SearchForFriendForm(request.GET)

        if form.is_valid():

            try:
                user_search = form.cleaned_data.get('query_friend_search')
                users_found = User.objects.filter(username__icontains=user_search)
                if not users_found:
                    users_found = User.objects.filter(postal_code=user_search)
                    if not users_found:
                        users_found = User.objects.filter(location=user_search)

            except Exception as e:
                print(e)

            context = {
                'user_search' : user_search,
                'users_found': users_found,
                'form':form,
            }

        return render(request, 'friends/search_friends_result.html', context)

    else:

        form = SearchForFriendForm()

    return render(request, 'friends/search_friends_result.html', {'form':form})


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
        """Equivalent to context dict to use variables"""

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


class FriendRequestDeleteView(LoginRequiredMixin,DeleteView):
    """class view that handles the decline of a
    friend request"""

    models = FriendRequest
    context_object_name = 'friend_request'
    template_name = 'friends/friend_request_confirm_delete.html'
    success_url = reverse_lazy('friends:see_friend_request_list')

    def get_queryset(self):
        """Returns the list of items for this view.
        If a user clicks on the message, we update
        the field is_read of Messenger model"""

        friend_request = FriendRequest.objects.filter(receiver=self.request.user)
        return friend_request


@login_required
def accept_friend_request(request):
    """view to accept a friend request, only
    friend request with  is_active = True are shown
    to the user"""

    if request.method == "POST":
        sender_id = request.POST['from_user']
        receiver_id = request.POST['to_user']

        sender = User.objects.get(id=sender_id) # get user
        receiver = User.objects.get(id=receiver_id) # get friend
        sender.friends.add(receiver)  # add_receiver
        receiver.friends.add(sender) # add_sender

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

        messages.success(request, "You have accepted your friend requests")

    return render(request, 'animals/home.html', context)


class FriendListView(LoginRequiredMixin, ListView):
    """view for the user to see his list of friends"""

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

        # delete the friend request so user can add each other again
        fr = FriendRequest.objects.filter(sender=user, receiver=friend)
        fr.delete()

        # delete the relationship for each user
        fl = FriendList.objects.filter(user=user, friend=friend) #delete for user
        fl_friend = FriendList.objects.filter(user=friend, friend=user) #delete for friend
        fl.delete()
        fl_friend.delete()

        # remove the friend for the User for 'friends' attribute
        sender = User.objects.get(id=user)
        receiver = User.objects.get(id=friend)
        sender.friends.remove(receiver)  # delete_friend_of_user
        receiver.friends.remove(sender) # delete_user_for_friend

        messages.success(request, "You have deleted your friend")

        return redirect('animals:home')

    else:

        friends = FriendList.objects.filter(user=request.user).all()
        context = {
            'friends': friends,
        }

    return render(request, 'friends/friend_delete.html', context)

######### CATSITTER CLASS VIEWS ###############

class CatsitterCreateView(LoginRequiredMixin, CreateView):
    """view to create a new task there
    makes a post request and creates an item,
    CreateView gives us a model form"""

    model = Catsitter
    template_name = 'friends/catsitter_form.html'
    success_url = reverse_lazy('friends:catsitter_list')
    form_class = CreateCatsitterForm

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that belong to a given user"""

        kwargs = super(CatsitterCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CatsitterCreateView, self).form_valid(form)

class CatsitterList(LoginRequiredMixin, ListView):
    """CBV for catsitter list available for user"""

    model = Catsitter
    context_object_name = "catsitters"
    template_name = 'friends/catsitter_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if Catsitter.objects.filter(is_owned=self.request.user).exists():
            context["catsitters"] = context["catsitters"].filter(is_owned=self.request.user)
        elif Catsitter.objects.filter(is_catsitter=self.request.user).exists():
            context["catsitters"] = context["catsitters"].filter(is_catsitter=self.request.user)
        return context

@login_required
def delete_catsitter_request(request):
    """ Delete a catsitter requests"""

    if request.method == "POST":
        user =  request.POST['user']
        friend = request.POST['to_delete_catsitter']
    try:
        Catsitter.objects.filter(is_owned=user, is_catsitter=friend).first().delete()
    except ObjectDoesNotExist as e:
        pass

    return redirect('friends:catsitter_list')

@login_required
def catsitter_get_cat_info(request, pk):
    """if the user is is_catsitter, then
    he can access all the data of the cat
    that he needs to take care of"""

    pet = Pet.objects.get(pk=pk)
    healthbook = HealthBook.objects.filter(pet=pet.pk)
    schedule = Schedule.objects.filter(pet=pet.pk).order_by("time")

    context = {
        'pet': pet,
        'healthbook': healthbook,
        'schedule': schedule,
    }

    return render(request, 'friends/catsitter_cat_info.html', context)



# utilisateur qui a appartient le chat
# autre utilisateur qui s'ccoupe du chat
# date début
# date fin

# is_active = False ou True (False quand le temps définit est passé)
# mieux que de supprimer la ligne dans la base de données

# interface : permet de voir que ce qui est actif
# Chaque jour, Django on vérifie avec une méthode

# Django Celery - pour se faire
# Django façon native
# Tâche cron qui peut exécuter : on peut aussi l'activer avec Django Celery

# Sur un serveur, je vais exécuté une tâche

# Au niveau application

# Mettre derniere version sur Github

# Quand je serai en production :

    # En production, on utilise pas l'imageField de Django
    # Les images que les utilisateurs
    # sont sauvegarder dans un autre serveur par exemple
    # amazon S3

    # mon serveur application est sur Linux
    # et on peut sauver les images dans un
    # bucket Amazon S3
    # tout ce qui est fichier uploader
    # on peut créer des buckets 'images, animals'
    # tout les uploads vont sur Amazon S3 du coup,
    # ça nous permet d'avoir une flexibilité

    # Pour éviter ce problème en production :
    # ON sauvegarde les images sur une instance externalisé

    # Google Storage aussi existe et Amazon S3
    # Si on a les images sauver sur un serveur de déploiement,

    # Ce que je peux faire :
    # Les éléments de mon image : on créer un compte amazon S3 ou Google Storage
    # on créer son compte
    # Google Storage : créer des buckets (animaux, users)
    # on a des librairies qui peuvent de façon automatique
#
# voir PYENV : plusieurs version, plusieurs version de python
# meilleure gestion, et d'avoir plusieurs versiuon depYthon de facon isolé
