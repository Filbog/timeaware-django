from django.test import TestCase
from django.urls import reverse
from accounts.models import CustomUser
from core.forms import ActivityForm
from core.models import Activity, ActivityInstance


class TestForms(TestCase):

    def test_activity_form_valid_data(self):
        form = ActivityForm(
            data={
                "title": "Test Activity",
                "type": "positive",
                "description": "This is a test description",
            }
        )

        self.assertTrue(form.is_valid())

    def test_activity_form_invalid_data(self):
        form = ActivityForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)  # Title and type are required

    def test_activity_form_labels(self):
        form = ActivityForm()
        self.assertEqual(
            form.fields["description"].label,
            "Description (optional) - e.g. state why you want to track this activity",
        )
