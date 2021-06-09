from django.shortcuts import render
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
    fields = ('title','description','complete',)
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
    content_object_name = 'task' #changed from "objects" to "tasks" for variable in template
    success_url = reverse_lazy('schedules:task_list')


######################################################
############## SCHEDULE CAT SECTION ##################
######################################################

# CBGV
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

# CBGV
class SchedulePetList(LoginRequiredMixin, ListView):
    """view to see tasks linked to a cat"""

    model = Schedule
    content_object_name = 'schedules'
    template_name = "schedules/schedule_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["schedules"] = Schedule.objects.filter(cat__owner=self.request.user)
        return context


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


def search(request):
    """view that corresponds to the search bar zone,
    that allows to retrieve data schedule from a cat
    from the DB according the cat name"""

    form = SearchPetScheduleForm()

    if request.method == "GET":
        form = SearchPetScheduleForm(request.GET)

        if form.is_valid():
            cat = form.cleaned_data.get("query_search")
            cat_schedule_found = Schedule.objects.filter(
                cat__name__startswith = cat
            )

            context = {
                'cat_searched': cat,
                'cat_schedule_found':cat_schedule_found
            }

            return render(request, 'schedules/schedule_result.html', context)
    else:
        form = SearchPetScheduleForm()

    return render(request, 'schedules/schedule_search.html', {'form' : form})

    # context = {}
    # form = SearchPetScheduleForm()

    # if request.method == "GET":
    #     form = SearchPetScheduleForm(request.GET)

    #     if form.is_valid():
    #         cat = form.cleaned_data.get("query_search")
    #         cat_found = Pet.objects.get_object_or_404(cat_name__icontains=cat)
    #         cat_schedule = Schedule.objects.filter(cat=cat_found)

    #         context = {
    #             'cat_schedule': cat_schedule,
    #         }

    #         return  render(request, 'schedules/schedule_result.html', context)

#################################################
########## PRACTICE SCHEDULE CAT SECTION ########
#################################################

# CBGV
# class SchedulePetCreate(LoginRequiredMixin,CreateView):
#     """view to create a schedule for one cat"""

#     model = Schedule
#     form_class = CreateScheduleForPet
#     template_name = 'schedules/schedule_form.html'
#     success_url = reverse_lazy('schedules:schedule_list')


# # CBGV
# class SchedulePetList(LoginRequiredMixin, ListView):
#     """view to see tasks linked to a cat"""

#     model = Schedule
#     content_object_name = 'schedules'
#     template_name = "schedules/schedules_list.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["schedules"] = Schedule.objects.filter(cat__owner=self.request.user)
#         return context


# def show_list_schedule(request):
#     """view to see list of schedules for a cat"""

#     schedules = Schedule.objects.filter(cat__owner=request.user)
#     context = {
#         'schedules':schedules
#     }

#     return render(request, 'schedules/show_schedule.html', context)



    # def get_queryset(self):
    #     return self.model.objects.filter(cat__owner=self.request.user)

    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object(queryset=Publisher.objects.all())
    #     return super().get(request, *args, **kwargs)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['publisher'] = self.object
    #     return context

    # def get_queryset(self):
    #     return self.object.book_set.all()
