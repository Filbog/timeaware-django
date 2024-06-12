from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.db.models import Sum


# flash messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages


from .models import Activity, ActivityInstance
from .forms import ActivityForm, TrackerForm


class AuthMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.username == self.get_object().owner.username


class CustomLoginRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "You need to log in to access this page.")
            return redirect(
                "login"
            )  # Ensure 'login' is the name of your login URL pattern
        return super().dispatch(request, *args, **kwargs)


class HomePageView(TemplateView):
    template_name = "home.html"


class ActivityGet(ListView):
    model = Activity
    template_name = "activity_list.html"

    def get_queryset(self):
        return Activity.objects.filter(owner=self.request.user).order_by("-date_added")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ActivityForm()
        return context


class ActivityPost(SuccessMessageMixin, FormView):
    # model = Activity
    form_class = ActivityForm
    template_name = "activity_list.html"
    success_message = "Activity created!"

    def post(self, request, *args, **kwargs):
        # self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        activity = form.save(commit=False)
        activity.owner = self.request.user
        activity.save()
        # messages.success(self.request, "Activity created!")
        return super().form_valid(form)

    def get_success_url(self):
        # activity = self.object
        return reverse("activity_list")


class ActivityListView(CustomLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = ActivityGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ActivityPost.as_view()
        return view(request, *args, **kwargs)


class ActivityStatisticsView(LoginRequiredMixin, AuthMixin, DetailView):
    model = Activity
    template_name = "activity_statistics.html"


class ActivityUpdateView(
    LoginRequiredMixin, AuthMixin, SuccessMessageMixin, UpdateView
):
    model = Activity
    fields = (
        "title",
        "description",
        "type",
    )
    template_name = "activity_edit.html"
    success_url = reverse_lazy("activity_list")
    success_message = "Activity updated!"


class ActivityDeleteView(
    LoginRequiredMixin, AuthMixin, SuccessMessageMixin, DeleteView
):
    model = Activity
    template_name = "activity_delete.html"
    success_url = reverse_lazy("activity_list")
    success_message = "Activity deleted!"


class ActivityTrackView(CustomLoginRequiredMixin, CreateView):
    model = ActivityInstance
    fields = ["start_time", "end_time", "duration"]
    template_name = "activity_track.html"
    success_url = reverse_lazy("activity_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        activity = get_object_or_404(Activity, pk=self.kwargs["pk"])
        context["activity_id"] = activity.id
        context["activity_title"] = activity.title
        return context

    def form_valid(self, form):
        form.instance.activity_id = self.kwargs["pk"]
        return super().form_valid(form)


class ActivityStatisticsView(TemplateView):
    template_name = "activity_statistics.html"

    def get_context_data(self, **kwargs):
        # get the 'original' data
        context = super().get_context_data(**kwargs)
        # get the id of the activity
        activity_id = self.kwargs["pk"]
        # get activity instances data
        activity_data = (
            ActivityInstance.objects.filter(activity_id=activity_id)
            .values("start_time__date")
            .annotate(total_duration=Sum("duration"))
            .order_by("start_time__date")
        )

        # prepare data for Chart.js
        labels = [
            entry["start_time__date"].strftime("%Y-%m-%d") for entry in activity_data
        ]
        data = [entry["total_duration"] for entry in activity_data]
        context["labels"] = labels
        print(type(labels[0]))
        context["data"] = data
        context["activity_name"] = Activity.objects.get(pk=activity_id).title
        print(context)
        return context


# test flash messages
def test_message(request):
    messages.success(request, "Test message!")
    return redirect("activity_list")
