from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import CustomUser
from core.models import Activity, ActivityInstance
from core.forms import ActivityForm


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpass", email="user@example.com"
        )
        self.different_user = CustomUser.objects.create_user(
            username="diffuser", password="diffpass", email="diffuser@example.com"
        )
        self.client.login(username="testuser", password="testpass")
        self.activity = Activity.objects.create(
            owner=self.user, title="Test Activity", type="neutral"
        )

    def test_activity_list_view(self):
        response = self.client.get(reverse("activity_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "activity_list.html")

    def test_activity_statistics_view(self):
        response = self.client.get(
            reverse("activity_statistics", args=[self.activity.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "activity_statistics.html")

    def test_activity_update_view(self):
        response = self.client.get(reverse("activity_edit", args=[self.activity.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "activity_edit.html")
        response = self.client.post(
            reverse("activity_edit", args=[self.activity.pk]),
            {"title": "Updated Activity", "type": "positive"},
        )
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.activity.refresh_from_db()
        self.assertEqual(self.activity.title, "Updated Activity")
        self.assertEqual(self.activity.type, "positive")

    def test_activity_delete_view(self):
        response = self.client.get(reverse("activity_delete", args=[self.activity.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "activity_delete.html")
        response = self.client.post(reverse("activity_delete", args=[self.activity.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect after successful delete
        with self.assertRaises(Activity.DoesNotExist):
            Activity.objects.get(pk=self.activity.pk)

    def test_activity_track_view(self):
        response = self.client.get(reverse("activity_track", args=[self.activity.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "activity_track.html")
        response = self.client.post(
            reverse("activity_track", args=[self.activity.pk]),
            {
                "start_time": "2023-01-01T10:00:00Z",
                "end_time": "2023-01-01T11:00:00Z",
                "duration": 60,
            },
        )
        self.assertEqual(
            response.status_code, 302
        )  # Redirect after successful creation
        activity_instance = ActivityInstance.objects.get(activity=self.activity)
        self.assertEqual(activity_instance.duration, 60)

    def test_activity_toggle_favorite_view(self):
        response = self.client.post(
            reverse("activity_favorite_toggle", args=[self.activity.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.activity.refresh_from_db()
        self.assertTrue(self.activity.favorite)
        response = self.client.post(
            reverse("activity_favorite_toggle", args=[self.activity.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.activity.refresh_from_db()
        self.assertFalse(self.activity.favorite)

    def test_stats_view_authorization(self):
        self.client.login(username="diffuser", password="diffpass")
        stats_response = self.client.get(
            reverse("activity_statistics", args=[self.activity.pk])
        )
        self.assertEqual(stats_response.status_code, 403)

        track_response = self.client.get(
            reverse("activity_track", args=[self.activity.pk])
        )
        self.assertEqual(track_response.status_code, 403)

        edit_response = self.client.get(
            reverse("activity_edit", args=[self.activity.pk])
        )
        self.assertEqual(edit_response.status_code, 403)

        delete_response = self.client.get(
            reverse("activity_delete", args=[self.activity.pk])
        )
        self.assertEqual(delete_response.status_code, 403)

    def test_activity_create_view_get(self):
        response = self.client.get(reverse("activity_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "activity_list.html")
        self.assertIsInstance(response.context["form"], ActivityForm)

    def test_activity_create_view_post_valid(self):
        response = self.client.post(
            reverse("activity_list"),
            {
                "title": "New Activity",
                "type": "positive",
                "description": "A new activity",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Activity.objects.filter(title="New Activity").exists())

    def test_activity_create_view_post_invalid(self):
        response = self.client.post(
            reverse("activity_list"),
            {
                "title": "",
                "type": "",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Activity.objects.filter(title="").exists())

    def test_activity_track_view_get(self):
        response = self.client.get(reverse("activity_track", args=[self.activity.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "activity_track.html")

    def test_activity_track_view_post_valid(self):
        response = self.client.post(
            reverse("activity_track", args=[self.activity.pk]),
            {
                "start_time": "2023-01-01T10:00:00Z",
                "end_time": "2023-01-01T11:00:00Z",
                "duration": 60,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            ActivityInstance.objects.filter(activity=self.activity).exists()
        )

    def test_activity_track_view_post_invalid(self):
        response = self.client.post(
            reverse("activity_track", args=[self.activity.pk]),
            {"start_time": "", "end_time": "", "duration": ""},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            ActivityInstance.objects.filter(activity=self.activity).exists()
        )
