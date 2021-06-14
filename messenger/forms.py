from django import forms
from django.forms import CheckboxSelectMultiple

from users.models import User
from .models import Messenger


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

        # self.fields['receiver'].queryset = Messenger.objects.filter(
        #     receiver__username=self.request.user)

# ERROR MUST BE AN INSTANCE OF USER AND NOT MESSENGER 


    class Meta:

        model = Messenger
        fields = ('sender','receiver', 'subject', 'content',)

        follower = CustomModelMultipleChoiceField(
        queryset=None,
        widget=CheckboxSelectMultiple
        )


    # def get_object(self, queryset=None):
    #     return Messenger.objects.get(subject=self.kwargs.get("subject"))


# class CreateReplyMessageForUser(forms.ModelForm):
#     """method to create a custom form
#     to create a schedule for a cat
#     The idea; is that the user can only see
#     his objects"""

#     def __init__(self, *args, **kwargs):
#         """ Grants access to the request object so that only members
#         of the current user are given as options"""

#         self.request = kwargs.pop('request')
#         super(CreateReplyMessageForUser, self).__init__(*args, **kwargs)
        
#         self.fields['sender'].queryset = User.objects.filter(
#             username = self.request.user)
        
#         self.fields['receiver'].queryset = Messenger.objects.filter(
#             receiver = self.request.user)

#     class Meta:

#         model = Messenger
#         fields = ('sender','receiver', 'subject', 'content',)

#         follower = CustomModelMultipleChoiceField(
#         queryset=None,
#         widget=CheckboxSelectMultiple
#         )