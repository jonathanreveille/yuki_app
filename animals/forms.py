from django import forms

from .models import Pet

class PetCreationForm(forms.ModelForm):
    """forms to create an animal for a owner"""
    
    class Meta:
        model = Pet
        fields =  ("name", "age", "weight", "specie")
