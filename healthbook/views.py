from healthbook.forms import CreateHealthBookForPet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import HealthBook, Medication
from .forms import CreateHealthBookForPet, CreateMedicationForPet


class HealthBookListView(LoginRequiredMixin, ListView):
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
        return context


class HealthBookCreateView(LoginRequiredMixin, CreateView):
    """view to create pet healthbook"""

    model = HealthBook 
    form_class = CreateHealthBookForPet
    template_name = 'healthbook/healthbook_form.html'
    success_url = reverse_lazy('healthbook:healthbook_list')

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that belong to a given user"""

        kwargs = super(HealthBookCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    
class HealthBookUpdateView(LoginRequiredMixin, UpdateView):
    """update a healthbook of pet"""
    
    model = HealthBook
    fields = ('pet', 'sterilize', 'vaccine',
                    'last_vaccine','next_vaccine',
                    'veterinary_name','veterinary_phone',)
    success_url = reverse_lazy('healthbook:healthbook_list')


####################################
######### MEDICATION ZONE ##########
####################################

class MedicationListView(LoginRequiredMixin, ListView):
    """view to see all medications for a pet"""
    model = Medication
    context_object_name = 'medication' 
    template_name = 'healthbook/medication_list.html'

    def get_context_data(self, **kwargs):
        """equivalent to context dict to use variables"""
        context = super().get_context_data(**kwargs)
        context["medication"] = Medication.objects.filter(
            pet__owner=self.request.user)
        return context


class MedicationCreateView(LoginRequiredMixin, CreateView):
    """view to create a new medication sheet
    for the pet"""

    model = Medication
    form_class = CreateMedicationForPet
    template_name = 'healthbook/medication_form.html'
    success_url = reverse_lazy('healthbook:medication_list')

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that belong to a given user"""

        kwargs = super(MedicationCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class MedicationUpdateView(LoginRequiredMixin, UpdateView):
    """view to update the medication fields for
    a pet, it uses healthbook_form.html with all
    the data from the creation that the user can modify"""

    model = Medication
    fields = ('pet', 'med_name',
                'med_start', 'med_end','time','dosage')
    success_url = reverse_lazy('healthbook:healthbook_list')


class MedicationDeleteView(LoginRequiredMixin, DeleteView):
    """view to ask for confirmation and it deletes
    a medication treatment for a pet if user agrees"""

    model = Medication
    context_object_name = 'medication'
    template_name = 'healthbook/medication_confirm_delete.html'
    success_url = reverse_lazy('healthbook:medication_list')