from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Pet
from .forms import PetCreationForm

# Create your views here.
def home(request):
    """method to get homepage"""
    return render(request, 'animals/home.html',)

@login_required
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

    return render(request, 'animals/pet_form.html', {'form':form})

@login_required
def see_pet(request):
    """view to allow the user
    to see his pets"""
    user = request.user
    user_pets = Pet.objects.filter(owner=user)

    context = {
        'user_pets' : user_pets,
    }

    return render(request, 'animals/see_pet.html', context)


class PetUpdateView(LoginRequiredMixin, UpdateView):
    """update a task"""
    
    model = Pet
    fields = ('name','age','weight',)
    success_url = reverse_lazy('animals:see_pet')


class PetDeleteView(LoginRequiredMixin, DeleteView):
    """update a task"""

    model = Pet
    content_object_name = 'pet'
    template_name = 'animals/pet_confirm_delete.html'
    success_url = reverse_lazy('animals:see_pet')
