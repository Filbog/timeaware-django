from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Activity
from .forms import ActivityForm


class AuthMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.username == self.get_object().owner.username


class HomePageView(TemplateView):
    template_name = "home.html"


class ActivityGet(ListView):
    model = Activity
    template_name = "activity_list.html"

    def get_queryset(self):
        return Activity.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ActivityForm()
        return context


class ActivityPost(FormView):
    # model = Activity
    form_class = ActivityForm
    template_name = "activity_list.html"

    def post(self, request, *args, **kwargs):
        # self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        activity = form.save(commit=False)
        activity.owner = self.request.user
        activity.save()
        return super().form_valid(form)

    def get_success_url(self):
        # activity = self.object
        return reverse("activity_list")


class ActivityListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = ActivityGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ActivityPost.as_view()
        return view(request, *args, **kwargs)


class ActivityStatisticsView(LoginRequiredMixin, AuthMixin, DetailView):
    model = Activity
    template_name = "activity_statistics.html"


class ActivityUpdateView(LoginRequiredMixin, AuthMixin, UpdateView):
    model = Activity
    fields = (
        "title",
        "description",
        "type",
    )
    template_name = "activity_edit.html"


class ActivityDeleteView(LoginRequiredMixin, AuthMixin, DeleteView):
    model = Activity
    template_name = "activity_delete.html"
    success_url = reverse_lazy("activity_list")


# class ActivityCreateView(LoginRequiredMixin, CreateView):
#     model = Activity
#     form_class = ActivityForm
#     template_name = "activity_list.html"
#     success_url = reverse_lazy("activity_list")

#     def form_valid(self, form):
#         form.instance.owner = self.request.user
#         return super().form_valid(form)
