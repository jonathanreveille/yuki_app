from friends.models import FriendList
from django import forms
from django.forms import CheckboxSelectMultiple

from users.models import User
from .models import Messenger
from friends.models import FriendList
from notifications.models import Notification


class CustomModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, follower):
        """ Customises the labels for checkboxes"""
        return "%s" % follower.username

class CreateMessageForUser(forms.ModelForm):
    """method to create a message form
    for a user to send a message to another
    user"""

    def __init__(self, *args, **kwargs):
        """ Grants access to the request object so that only members
        of the current user are given as options"""

        self.request = kwargs.pop('request')
        super(CreateMessageForUser, self).__init__(*args, **kwargs)
        
        self.fields['sender'].queryset = User.objects.filter(
            username=self.request.user)

        user = User.objects.get(username__startswith=self.request.user)
        self.fields['receiver'].queryset = user.friends
        

    class Meta:

        model = Messenger
        fields = ('sender','receiver', 'subject', 'content',)

        follower = CustomModelMultipleChoiceField(
        queryset=None,
        widget=CheckboxSelectMultiple
        )


class CreateReplyMessageForUser(forms.ModelForm):
    """method to create a custom form
    to create a schedule for a cat
    The idea; is that the user can only see
    his objects"""

    def __init__(self, *args, **kwargs):
        """ Grants access to the request object so that only members
        of the current user are given as options"""

        self.request = kwargs.pop('request')
        super(CreateReplyMessageForUser, self).__init__(*args, **kwargs)
        
        self.fields['sender'].queryset = User.objects.filter(
            username = self.request.user)
        
        user = User.objects.get(username__startswith=self.request.user)
        self.fields['receiver'].queryset = user.friends


    class Meta:
        
        model = Messenger
        fields = ('sender','receiver', 'subject', 'content',)

        follower = CustomModelMultipleChoiceField(
        queryset=None,
        widget=CheckboxSelectMultiple
        )






    # def send_notification(self, message):
    #     """send notification once message is sent"""

    #     receiver = self.cleaned_data.get("receiver")
    #     friendd = User.objects.get(username__startswith=receiver) #works

    #     notification = Notification.objects.get_or_create(notification_type=2,
    #                                                     from_user=self.request.user,
    #                                                     to_user=friendd,
    #                                                     message=message)
    #     return notification


        # sender = self.cleaned_data.get("sender")
        # subject = self.cleaned_data.get("subject")
        # content = self.cleaned_data.get("content")
        # message = Messenger.objects.get(sender=sender, receiver=receiver,
        #                                 subject=subject, content=content)



        # self.fields['receiver'].queryset = User.objects.filter(username=friend)
    
        # user = User.objects.filter(username=self.request.user)
        # friends = user.friends.all()

        # self.fields['sender'].queryset =  friends

        # jonny = User.objects.filter(
        #     username__startswith =  "jonny",
        # )

        # self.fields['receiver'].queryset = jonny.friends.all()

        # user = User.objects.get(user=self.request.user)

        # self.fields['receiver'].queryset =

        # f = FriendList.objects.get(user=self.request.user)
        # friend = f.friend.username

        # self.fields['receiver'].queryset = User.objects.filter(username=friend)
        # Must be an intance of user...

        # line 30 : MULTIPLE VALUE ERROR IF MORE THAN ONE FRIEND
        # If user has only one friend, it works.
        # if  user has more than one friend (3 friends), there's a MultipleValue Error with get() method returns 3 instead of 1 
