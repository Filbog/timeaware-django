from django.test import SimpleTestCase
from django.urls import reverse

# Create your tests here.


class HomePageTests(SimpleTestCase):

    def test_homepage_view(self):
        response = self.client.get(reverse("home-redirect"))
        self.assertEqual(response.status_code, 302)
