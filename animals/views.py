from django.shortcuts import render, redirect

from .models import Pet
from users.models import User

from .forms import PetCreationForm
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.generic.edit  import CreateView
# from django.views.generic.list import ListView
# # from django.urls import reverse_lazy

# Create your views here.
def home(request):
    """method to get homepage"""
    return render(request, 'animals/home.html',)

def create_pet(request):
    """method to create animals
    from the user"""

    if request.method == "POST":
        form = PetCreationForm(request.POST)

        if form.is_valid():
            owner = request.user
            name = form.cleaned_data.get("name")
            weight = form.cleaned_data.get("weight")
            age = form.cleaned_data.get("age")
            specie = form.cleaned_data.get("specie")
            
            Pet.objects.get_or_create(
                name=name,
                weight=weight,
                age=age,
                specie=specie,
                owner=owner,
            )

        return redirect('animals:home')

    else:

        form = PetCreationForm()

    return render(request, 'animals/create_animal.html', {'form':form})

def see_pet(request):
    """view to allow the user
    to see his pets"""
    user = request.user
    user_pets = Pet.objects.filter(owner=user)

    context = {
        'user_pets' : user_pets,
    }

    return render(request, 'animals/see_pet.html', context)

