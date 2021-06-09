from django import forms
from django.forms import CheckboxSelectMultiple

from animals.models import Pet
from .models import Task, Schedule


class CustomModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, cat):
        """ Customises the labels for checkboxes"""
        return "%s" % cat.name

class CreateScheduleForPet(forms.ModelForm):
    """method to create a custom form
    to create a schedule for a cat
    The idea; is that the user can only see
    his objects"""

    def __init__(self, *args, **kwargs):
        """ Grants access to the request object so that only members
        of the current user are given as options"""

        self.request = kwargs.pop('request')
        super(CreateScheduleForPet, self).__init__(*args, **kwargs)
        
        self.fields['cat'].queryset = Pet.objects.filter(
            owner=self.request.user)

        self.fields['task'].queryset = Task.objects.filter(
            user=self.request.user)

    class Meta:

        model = Schedule
        fields = ('cat', 'task', 'time',)

        cat = CustomModelMultipleChoiceField(
        queryset=None,
        widget=CheckboxSelectMultiple
        )


class SearchPetScheduleForm(forms.Form):
    query_search = forms.CharField(label="Animal name",max_length=200)