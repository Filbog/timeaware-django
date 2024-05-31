from django.urls import path

from .views import (
    HomePageView,
    ActivityListView,
    ActivityStatisticsView,
    ActivityUpdateView,
    ActivityDeleteView,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("", HomePageView.as_view(), name="tracker"),
    path("", HomePageView.as_view(), name="about"),
    #
    path("activities/", ActivityListView.as_view(), name="activity_list"),
    path(
        "activities/<int:pk>",
        ActivityStatisticsView.as_view(),
        name="activity_statistics",
    ),
    path(
        "activities/<int:pk>/edit/", ActivityUpdateView.as_view(), name="activity_edit"
    ),
    path(
        "activities/<int:pk>/delete/",
        ActivityDeleteView.as_view(),
        name="activity_delete",
    ),
]
