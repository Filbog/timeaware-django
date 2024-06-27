from django.urls import path
from django.views.generic import TemplateView

from .views import (
    HomeRedirectView,
    ActivityListView,
    ActivityStatisticsView,
    ActivityUpdateView,
    ActivityDeleteView,
    ActivityTrackView,
    ActivityToggleFavoriteView,
    test_message,
)

urlpatterns = [
    path("", HomeRedirectView.as_view(), name="home-redirect"),
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),
    #
    path("activities/", ActivityListView.as_view(), name="activity_list"),
    path(
        "activities/<int:pk>/",
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
    path(
        "activities/<int:pk>/favorite/",
        ActivityToggleFavoriteView.as_view(),
        name="activity_favorite_toggle",
    ),
    path("test-message/", test_message, name="test_message"),
    # path("activities/create/", ActivityCreateView.as_view(), name="activity_create"),
]
