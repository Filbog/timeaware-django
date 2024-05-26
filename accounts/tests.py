from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

# Create your tests here.


class CustomUserTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="testuser", password="testpass", email="email@example.com"
        )

        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.email, "email@example.com")
        self.assertEqual(user.goal, "")

    def test_create_user_with_goal(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="testuser",
            password="testpass",
            email="email@example.com",
            goal="test goal",
        )

        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.goal, "test goal")


class CustomAdminTests(TestCase):
    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username="superadmin", password="superpass", email="admin@example.com"
        )

        self.assertEqual(admin_user.username, "superadmin")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertEqual(admin_user.email, "admin@example.com")


class SignupPageTests(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/accounts/signup/")
        self.assertEqual(response.status_code, 200)

    def test_signup_view_name(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_signup_form(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "testuser1",
                "email": "test1@example.com",
                "password1": "testpaSS123",
                "password2": "testpaSS123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, "testuser1")
        self.assertEqual(get_user_model().objects.all()[0].email, "test1@example.com")
