from django import forms
from django.forms import CheckboxSelectMultiple

from animals.models import Pet
from .models import Task, Schedule


class CustomModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, pet):
        """ Customises the labels for checkboxes"""
        return "%s" % pet.name

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
        
        self.fields['pet'].queryset = Pet.objects.filter(
            owner=self.request.user)

        self.fields['task'].queryset = Task.objects.filter(
            user=self.request.user)

    class Meta:

        model = Schedule
        fields = ('pet', 'task', 'time',)

        pet = CustomModelMultipleChoiceField(
        queryset=None,
        widget=CheckboxSelectMultiple
        )


class SearchPetScheduleForm(forms.Form):
    query_search = forms.CharField(label="Type animal name for full schedule",max_length=200)