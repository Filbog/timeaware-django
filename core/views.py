from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy

from .models import Activity


class HomePageView(TemplateView):
    template_name = "home.html"


class ActivityListView(ListView):
    model = Activity
    template_name = "activity_list.html"


class ActivityStatisticsView(DetailView):
    model = Activity
    template_name = "activity_statistics.html"


class ActivityUpdateView(UpdateView):
    model = Activity
    fields = (
        "title",
        "description",
        "type",
    )
    template_name = "activity_edit.html"


class ActivityDeleteView(DeleteView):
    model = Activity
    template_name = "activity_delete.html"
    success_url = reverse_lazy("activity_list")


class ActivityCreateView(CreateView):
    model = Activity
    template_name = "activity_create.html"
    fields = ("title", "description", "type")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
