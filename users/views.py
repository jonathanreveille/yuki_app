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
        user_form = UserChangeForm(request.POST, instance=request.user)

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


# @login_required
# def schedule_search(request):    
#     """view that corresponds to the search bar zone,
#     that allows to retrieve data schedule from a cat
#     from the DB according the cat name"""

#     if request.method == "GET":
#         form = SearchForUserForm(request.GET)

#         if form.is_valid():
            

    #     if form.is_valid():
    #         pet = form.cleaned_data.get("query_search")
    #         pet_schedule_found = Schedule.objects.filter(
    #             pet__name__startswith = pet,
    #             pet__owner= request.user,
    #         ).order_by('time')

    #         context = {
    #             'pet_searched': pet,
    #             'pet_schedule_found':pet_schedule_found
    #         }

    #         return render(
    #             request, 'schedules/schedule_result.html', context
    #             )
    # else:
    #     form = SearchPetScheduleForm()

    # return render(
    #     request, 'schedules/schedule_search.html', {'form' : form}
    #     )
