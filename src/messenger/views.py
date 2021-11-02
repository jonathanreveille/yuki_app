from users.models import User
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView
from django.urls import reverse_lazy

from .models import Messenger
from .forms import CreateMessageForUser, CreateReplyMessageForUser
from notifications.models import Notification


class MessengerListView(LoginRequiredMixin, ListView):

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


class MessengerCreateView(LoginRequiredMixin, CreateView):

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
            message, created = Messenger.objects.get_or_create(
                sender=sender,
                receiver=receiver,
                subject=subject,
                content=content)
            friend_id = User.objects.get(username__startswith=receiver)
            if created:
                Notification.objects.get_or_create(notification_type=2,
                                                   from_user=self.request.user,
                                                   to_user=friend_id,
                                                   message=message)
        return redirect('messenger:message_list')

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
        This is necessary to only display members that
        belong to a given user"""

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


class MessengerCreateReplyView(LoginRequiredMixin, CreateView):
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
            message, created = Messenger.objects.get_or_create(
                sender=sender,
                receiver=receiver,
                subject=subject,
                content=content)
            friendd = User.objects.get(username__startswith=receiver)
            if created:
                Notification.objects.get_or_create(notification_type=2,
                                                   from_user=self.request.user,
                                                   to_user=friendd,
                                                   message=message)
        return redirect('messenger:message_list')

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that
         belong to a given user"""

        kwargs = super(MessengerCreateReplyView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
