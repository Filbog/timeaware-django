from django.urls import path

from .views import HomePageView, ActivityListView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    # path("", HomePageView.as_view(), name="dashboard"),
    path("", HomePageView.as_view(), name="tracker"),
    path("", HomePageView.as_view(), name="statistics"),
    path("", HomePageView.as_view(), name="about"),
    #
    path("", ActivityListView.as_view(), name="activity_list"),
]
