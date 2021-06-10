from healthbook.forms import CreateHealthBookForPet
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import HealthBook, Medication
from animals.models import Pet
from .forms import CreateHealthBookForPet


class HealthBookList(LoginRequiredMixin, ListView):
    """view to see HealthBook information
    about the user's pet"""
    model = HealthBook
    context_object_name = "healthbook"
    template_name = 'healthbook/healthbook_list.html'

    def get_context_data(self, **kwargs):
        """equivalent to context dict to use variables"""
        context = super().get_context_data(**kwargs)
        context["healthbook"] = HealthBook.objects.filter(
            pet__owner=self.request.user)
        context["color"] = "red"
        return context


class HealthBookCreate(LoginRequiredMixin, CreateView):
    """view to create pet healthbook"""

    model = HealthBook 
    form_class = CreateHealthBookForPet
    template_name = 'healthbook/healthbook_form.html'
    success_url = reverse_lazy('healthbook:healthbook_list')

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that belong to a given user"""

        kwargs = super(HealthBookCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    
class HealthBookUpdate(LoginRequiredMixin, UpdateView):
    pass


####################################
######### MEDICATION ZONE ##########
####################################

class MedicationList(LoginRequiredMixin, ListView):
    pass

class MedicationCreate(LoginRequiredMixin, CreateView):
    pass

class MedicationUpdate(LoginRequiredMixin, UpdateView):
    pass

class MedicationDetail(LoginRequiredMixin,DetailView):
    pass

class MedicationDelete(LoginRequiredMixin, DeleteView):
    pass


