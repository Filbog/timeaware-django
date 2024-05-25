from django.test import TestCase
from django.contrib.auth import get_user_model

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
