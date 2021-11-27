from schedules.forms import CustomModelMultipleChoiceField
from django import forms
from django.forms import CheckboxSelectMultiple

from animals.models import Pet
from friends.models import Catsitter
from users.models import User


class SearchForFriendForm(forms.Form):
    query_friend_search = forms.CharField(label="",
                                          max_length=255,
                                          widget=forms.TextInput(
                                              attrs={
                                                  'class': 'user_search',
                                              }))


class CreateCatsitterForm(forms.ModelForm):
    """method to create a custom form
    to create a schedule for a cat
    The idea; is that the user can only see
    his objects"""

    def __init__(self, *args, **kwargs):
        """ Grants access to the request object so that only members
        of the current user are given as options"""

        self.request = kwargs.pop('request')
        super(CreateCatsitterForm, self).__init__(*args, **kwargs)
        user = User.objects.get(username__startswith=self.request.user)
        self.fields['is_catsitter'].queryset = user.friends
        self.fields['is_owned'].queryset = User.objects.filter(
            username=self.request.user)
        self.fields['pet'].queryset = Pet.objects.filter(
            owner=self.request.user)

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start')
        end = cleaned_data.get('end')
        if start > end:
            raise forms.ValidationError(
                'Start date should always be lower than end date.')

    class Meta:
        model = Catsitter
        fields = ('is_owned', 'is_catsitter', 'pet', 'start', 'end')
        widgets = {
            'start': forms.DateTimeInput(attrs={'class': 'datetime-input'}),
            'end': forms.DateTimeInput(attrs={'class': 'datetime-input'})
        }
        catsitter = CustomModelMultipleChoiceField(
            queryset=None,
            widget=CheckboxSelectMultiple)
