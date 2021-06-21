from users.models import User
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView #UpdateView
from django.urls import reverse_lazy

from .models import Messenger
from .forms import CreateMessageForUser, CreateReplyMessageForUser
from notifications.models import Notification


# Create your views here.
class MessengerListView(LoginRequiredMixin,ListView):
    
    model = Messenger
    context_object_name = "messages"
    template_name = 'messenger/message_list.html'

    def get_context_data(self, **kwargs):
        """equivalent to context dict to use variables
        to retrieve only the data we want to display
        for the user"""
        
        context = super().get_context_data(**kwargs)
        context["messages"] = Messenger.objects.filter(
            receiver__username=self.request.user)
        return context

class MessengerCreateView(LoginRequiredMixin,CreateView):

    model = Messenger
    form_class = CreateMessageForUser
    template_name = 'messenger/messenger_form.html'
    

    def form_valid(self, form):
        """check if the form is valid"""

        if form.is_valid():
            receiver = form.cleaned_data.get("receiver")
            sender = form.cleaned_data.get("sender")
            subject = form.cleaned_data.get("subject")
            content = form.cleaned_data.get("content")
            message, created = Messenger.objects.get_or_create(sender=sender, receiver=receiver,
                                            subject=subject, content=content)

            friend_id = User.objects.get(username__startswith=receiver) #works

            if created:
                Notification.objects.get_or_create(notification_type=2,
                                                        from_user=self.request.user,
                                                        to_user=friend_id,
                                                        message=message)
        return redirect('messenger:message_list')


    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that belong to a given user"""

        kwargs = super(MessengerCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class MessengerDeleteView(LoginRequiredMixin, DeleteView):

    model = Messenger
    context_object_name = 'messages'
    template_name = 'messenger/messenger_confirm_delete.html'
    success_url = reverse_lazy('messenger:message_list')

class MessengerDetailView(LoginRequiredMixin, DetailView):

    model = Messenger
    context_object_name = 'message'
    template_name = 'messenger/messenger_detail.html'

    def get_queryset(self):
        """Return the list of items for this view.
        If a user clicks on the message, we update
        the field is_read of Messenger model"""

        message = Messenger.objects.filter(receiver=self.request.user)
        # mark as reads if `user` visits this message page detail
        message.update(is_read=True)
        return message


class  MessengerCreateReplyView(LoginRequiredMixin, CreateView):
    """class to create a reply message from an
    incoming message"""

    model = Messenger
    form_class = CreateReplyMessageForUser
    template_name = 'messenger/messenger_reply_form.html'
    success_url = reverse_lazy('messenger:message_list')

    def form_valid(self, form):
        """check if the form is valid"""

        if form.is_valid():
            receiver = form.cleaned_data.get("receiver")
            sender = form.cleaned_data.get("sender")
            subject = form.cleaned_data.get("subject")
            content = form.cleaned_data.get("content")
            message, created = Messenger.objects.get_or_create(sender=sender, receiver=receiver,
                                            subject=subject, content=content)

            friendd = User.objects.get(username__startswith=receiver) #works

            if created:
                Notification.objects.get_or_create(notification_type=2,
                                                        from_user=self.request.user,
                                                        to_user=friendd,
                                                        message=message)
        return redirect('messenger:message_list')


    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that belong to a given user"""

        kwargs = super(MessengerCreateReplyView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs






    # def form_valid(self, form):
    #     """check if the form is valid"""
    #     form.instance.user = self.request.user
    #     form.send_notification(self.object)
    #     return super(MessengerCreateView, self).form_valid(form)

    # def send_notifications(self, form):
    #     """check if the form is valid"""
    #     if form.form_valid:
    #         receiver = self.cleaned_data.get("receiver")
    #         sender = self.cleaned_data.get("sender")
    #         subject = self.cleaned_data.get("subject")
    #         content = self.cleaned_data.get("content")
    #         message = Messenger.objects.get(sender=sender, receiver=receiver,
    #                                         subject=subject, content=content)

    #         friendd = User.objects.get(username__startswith=receiver) #works
    #         notification = Notification.objects.get_or_create(notification_type=2, from_user=self.request.user, to_user=friendd, message=message)
    #     return notification



        # form.instance.user = self.request.user
        # self.object = form.save()
        # Notification.objects.create(notification_type=2, from_user=self.request.user, to_user=self.object["receiver"], message=self.object.id)
        # return redirect(self.get_sucess_url())


    # def form_valid(self,request, form):
    #     """check if all fields are complete"""
    #     self.form = CreateMessageForUser()
    #     if request.method == "POST":
    #         self.form = CreateMessageForUser(request.POST)
    #         if self.form.is_valid():
    #             u = self.form.cleaned_data.get["user"]
    #             f = self.form.cleaned_data.get["receiver"]
    #             friend = User.object.get(username__startswith=f)
    #             user = User.object.get(username__startswith=u)
    #             self.object = self.form.save()
    #             Notification.objects.get_or_create(notification_type=2, from_user=friend, to_user=user, message=self.object)
    #         return redirect(self.get_sucess_url())