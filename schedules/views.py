from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Schedule, Task
from schedules.forms import CreateScheduleForPet, SearchPetScheduleForm

# Create your views here.
class TaskList(LoginRequiredMixin, ListView):
    """view for the to do section of the 
    application"""
    
    model = Task
    context_object_name = 'tasks'
    template_name= 'schedules/task_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = context["tasks"].filter(user=self.request.user)
        context["count"] = context["tasks"].filter(complete=False).count()
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    """view for task details"""
    
    model = Task
    context_object_name = 'task'
    template_name = 'schedules/task_detail.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    """view to create a new task there 
    makes a post request and creates an item,
    CreateView gives us a model form"""

    model = Task
    fields = ('title','category','description','complete')
    success_url = reverse_lazy('schedules:task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    """update a task"""
    
    model = Task
    fields = ('title','description','complete',)
    success_url = reverse_lazy('schedules:task_list')


class TaskDelete(LoginRequiredMixin, DeleteView):
    """view to delete items from list"""
   
    model = Task
    content_object_name = 'task'
    success_url = reverse_lazy('schedules:task_list')


######################################################
############## SCHEDULE CAT SECTION ##################
######################################################

class SchedulePetCreate(LoginRequiredMixin,CreateView):
    """view to create a schedule for one cat"""

    model = Schedule
    form_class = CreateScheduleForPet
    template_name = 'schedules/schedule_form.html'
    success_url = reverse_lazy('schedules:schedule_list')

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that belong to a given user"""

        kwargs = super(SchedulePetCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class ScheduleDetailView(LoginRequiredMixin, DetailView):
    """view to see the details about a task in
    the schedules"""

    model = Schedule
    context_object_name = 'schedule'
    template_name = 'schedules/schedule_detail.html'


class ScheduleDeleteView(LoginRequiredMixin, DeleteView):
    """view to delete a schedule created by
    the owner of a pet"""

    model = Schedule
    context_object_name = 'schedule'
    template_name = 'schedules/schedule_confirm_delete.html'
    success_url = reverse_lazy('schedules:schedule_list')

# CBGV
class SchedulePetList(LoginRequiredMixin, ListView):
    """view to see tasks linked to a cat"""

    model = Schedule
    content_object_name = 'schedules'
    template_name = "schedules/schedule_list.html"

    def get_context_data(self, **kwargs):
        """equivalent to context dict to use variables"""
        context = super().get_context_data(**kwargs)
        context["schedules"] = Schedule.objects.filter(
            cat__owner=self.request.user
            ).order_by('time')
        context["form"] = SearchPetScheduleForm()
        return context

@login_required
def schedule_search(request):    
    """view that corresponds to the search bar zone,
    that allows to retrieve data schedule from a cat
    from the DB according the cat name"""

    if request.method == "GET":
        form = SearchPetScheduleForm(request.GET)

        if form.is_valid():
            cat = form.cleaned_data.get("query_search")
            cat_schedule_found = Schedule.objects.filter(
                cat__name__startswith = cat,
                cat__owner= request.user,
            )

            context = {
                'cat_searched': cat,
                'cat_schedule_found':cat_schedule_found
            }

            return render(
                request, 'schedules/schedule_result.html', context
                )
    else:
        form = SearchPetScheduleForm()

    return render(
        request, 'schedules/schedule_search.html', {'form' : form}
        )
