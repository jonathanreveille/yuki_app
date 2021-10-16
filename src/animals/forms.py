from django import forms

from .models import Pet

class PetCreationForm(forms.ModelForm):
    """Forms to create an animal for a owner"""

    class Meta:
        model = Pet
        fields =  ("name", "age", "weight", "specie")


class PetEditForm(forms.Form):
    """Form to update the pet's profile picture"""
    avatar = forms.ImageField()

    class Meta:
        model = Pet
        fields = ("avatar",)
