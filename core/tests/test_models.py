from core.models import Activity, ActivityInstance
from django.test import TestCase, SimpleTestCase
from accounts.models import CustomUser
from django.utils import timezone


class ActivityModelTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpass", email="user@example.com"
        )

        self.activity = Activity.objects.create(
            owner=self.user, title="Test Activity", type="positive"
        )

        self.activity_with_description = Activity.objects.create(
            owner=self.user,
            title="Activity with description",
            type="neutral",
            description="test description",
        )

    def test_activity_creation(self):

        self.assertEqual(self.activity.title, "Test Activity")
        self.assertEqual(self.activity.owner.username, "testuser")
        self.assertEqual(self.activity.favorite, False)
        self.assertEqual(self.activity.description, "")

        self.assertEqual(self.activity_with_description.description, "test description")

    def test_activity_string_representation(self):
        self.assertEqual(str(self.activity), "Test Activity")

    def test_activity_type_choices(self):
        print("HELLO")
        self.activity.type = "positive"
        self.activity.save()
        self.assertEqual(self.activity.type, "positive")

    def test_date_added(self):
        self.assertIsNotNone(self.activity.date_added)
        self.assertTrue(
            timezone.now() - self.activity.date_added < timezone.timedelta(seconds=1)
        )

    def test_get_absolute_url(self):
        self.assertEqual(
            self.activity.get_absolute_url(),
            f"/activities/{self.activity.pk}/",
        )

    def test_activity_owner_relationship(self):
        self.assertEqual(self.activity.owner, self.user)


class ActivityInstanceModelTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpass"
        )
        self.activity = Activity.objects.create(owner=self.user, title="Test Activity")
        self.start_time = timezone.now()
        self.end_time = self.start_time + timezone.timedelta(hours=1)
        self.activity_instance = ActivityInstance.objects.create(
            activity=self.activity,
            start_time=self.start_time,
            end_time=self.end_time,
            duration=3600,
        )

    def test_activity_instance_creation(self):
        self.assertEqual(self.activity_instance.activity.title, "Test Activity")
        self.assertEqual(self.activity_instance.start_time, self.start_time)
        self.assertEqual(self.activity_instance.end_time, self.end_time)
        self.assertEqual(self.activity_instance.duration, 3600)

    def test_activity_instance_string_representation(self):
        self.assertEqual(str(self.activity_instance), "Test Activity instance")

    def test_duration_calculation(self):
        calculated_duration = (
            self.activity_instance.end_time - self.activity_instance.start_time
        ).total_seconds()
        self.assertEqual(self.activity_instance.duration, calculated_duration)

    def test_time_constraints(self):
        self.activity_instance.end_time = self.activity_instance.start_time
        self.activity_instance.save()
        self.assertEqual(
            self.activity_instance.end_time, self.activity_instance.start_time
        )

        with self.assertRaises(Exception):
            invalid_instance = ActivityInstance(
                activity=self.activity,
                start_time=self.start_time,
                end_time=self.start_time - timezone.timedelta(hours=1),
                duration=-60,
            )
            invalid_instance.save()

    def test_cascading_delete(self):
        self.activity.delete()
        with self.assertRaises(ActivityInstance.DoesNotExist):
            ActivityInstance.objects.get(pk=self.activity_instance.pk)
