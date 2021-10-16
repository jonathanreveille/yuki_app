from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction

from .forms import UserCreationForm, UserChangeForm

# Create your views here.
def register(request):
    """view to register user"""

    if request.method  == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            messages.success(request, f'Votre compte a été créé avec succès {username} avec adresse {email}! Vous pouvez maintenant vous connecter')
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form':form})

@login_required
def profile(request):
    return render(request, 'users/profile.html')

@login_required
@transaction.atomic
def edit_profile(request):
    
    if request.method == "POST":
        user_form = UserChangeForm(request.POST, request.FILES, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            return redirect('profile')
        else:
            UserChangeForm()

    else:
        user_form = UserChangeForm(instance=request.user)
        context = {
            'user_form':user_form,
        }
        return render(request, 'users/edit_profile.html', context)
