from django.urls import path

from .views import (
    HomePageView,
    ActivityListView,
    ActivityStatisticsView,
    ActivityUpdateView,
    ActivityDeleteView,
    ActivityTrackView,
    test_message,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
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
    path(
        "activities/<int:pk>/track/", ActivityTrackView.as_view(), name="activity_track"
    ),
    path("test-message/", test_message, name="test_message"),
    # path("activities/create/", ActivityCreateView.as_view(), name="activity_create"),
]
