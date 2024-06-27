from django.test import SimpleTestCase
from django.urls import reverse, resolve
from core.views import (
    HomeRedirectView,
    ActivityListView,
    ActivityStatisticsView,
    ActivityUpdateView,
    ActivityDeleteView,
    ActivityTrackView,
    ActivityToggleFavoriteView,
)
from django.views.generic import TemplateView


class TestUrls(SimpleTestCase):

    def test_home_redirect_url(self):
        url = reverse("home-redirect")
        self.assertEqual(resolve(url).func.view_class, HomeRedirectView)

    def test_about_url(self):
        url = reverse("about")
        self.assertEqual(resolve(url).func.view_class, TemplateView)

    def test_activity_list_url(self):
        url = reverse("activity_list")
        self.assertEqual(resolve(url).func.view_class, ActivityListView)

    def test_activity_statistics_url(self):
        url = reverse("activity_statistics", args=[1])
        self.assertEqual(resolve(url).func.view_class, ActivityStatisticsView)

    def test_activity_edit_url(self):
        url = reverse("activity_edit", args=[1])
        self.assertEqual(resolve(url).func.view_class, ActivityUpdateView)

    def test_activity_delete_url(self):
        url = reverse("activity_delete", args=[1])
        self.assertEqual(resolve(url).func.view_class, ActivityDeleteView)

    def test_activity_track_url(self):
        url = reverse("activity_track", args=[1])
        self.assertEqual(resolve(url).func.view_class, ActivityTrackView)

    def test_activity_favorite_toggle_url(self):
        url = reverse("activity_favorite_toggle", args=[1])
        self.assertEqual(resolve(url).func.view_class, ActivityToggleFavoriteView)
