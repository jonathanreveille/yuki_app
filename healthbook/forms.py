from django import forms
from django.forms import CheckboxSelectMultiple

from animals.models import Pet
from .models import HealthBook, Medication


class CustomModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, pet):
        """ Customises the labels for checkboxes"""
        return "%s" % pet.name


class CreateHealthBookForPet(forms.ModelForm):
    """method to create a custom form
    to create a schedule for a cat
    The idea; is that the user can only see
    his objects"""

    def __init__(self, *args, **kwargs):
        """ Grants access to the request object so that only members
        of the current user are given as options"""

        self.request = kwargs.pop('request')
        super(CreateHealthBookForPet, self).__init__(*args, **kwargs)
        
        self.fields['pet'].queryset = Pet.objects.filter(
            owner=self.request.user)

    class Meta:

        model = HealthBook
        fields = ('pet', 'sterilize', 'vaccine',
                    'last_vaccine','next_vaccine',
                    'veterinary_name','veterinary_phone',)

        pet = CustomModelMultipleChoiceField(
        queryset=None,
        widget=CheckboxSelectMultiple
        )


class CreateMedicationForPet(forms.ModelForm):
    """method to create a custom form
    to create a schedule for a cat
    The idea; is that the user can only see
    his objects"""

    def __init__(self, *args, **kwargs):
        """ Grants access to the request object so that only members
        of the current user are given as options"""

        self.request = kwargs.pop('request')
        super(CreateMedicationForPet, self).__init__(*args, **kwargs)
        
        self.fields['pet'].queryset = Pet.objects.filter(
            owner=self.request.user)

    class Meta:

        model = Medication
        fields = ('pet', 'med_name',
                'med_start', 'med_end','time','dosage')

        pet = CustomModelMultipleChoiceField(
        queryset=None,
        widget=CheckboxSelectMultiple)