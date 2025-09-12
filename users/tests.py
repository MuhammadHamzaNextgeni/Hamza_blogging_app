from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

# Create your testcase here

User = get_user_model()


class UserViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse("users:signup")
        self.login_url = reverse("users:login")
        self.logout_url = reverse("users:logout")
        self.dashboard_url = reverse("users:dashboard")

        # Create a test user
        self.user = User.objects.create_user(
            username="hamza",
            email="hamza@example.com",
            password="StrongPass123",
        )

    def test_home_view_renders(self):
        response = self.client.get(reverse("home"))  
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_signup_view_creates_user(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(User.objects.filter(username="newuser").exists()) 

    def test_signup_view_invalid_data(self):
        data = {
            "username": "",  
            "email": "bademail",
            "password1": "123",
            "password2": "456",
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)  
        self.assertContains(response, "form")  

    def test_login_view_valid_user(self):
        data = {"email": "hamza@example.com", "password": "StrongPass123"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 302)  
        self.assertIn("access_token", response.cookies)  
        self.assertIn("refresh_token", response.cookies)  

    def test_login_view_invalid_password(self):
        data = {"email": "hamza@example.com", "password": "WrongPass"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid email or password")

    def test_login_view_no_user_found(self):
        data = {"email": "nouser@example.com", "password": "pass"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No account found")

    def test_logout_view(self):
        self.client.force_login(self.user)  
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        # After logout, cookie should be cleared (empty string)
        self.assertEqual(response.cookies.get("access_token").value, "")
        self.assertEqual(response.cookies.get("refresh_token").value, "")

    def test_dashboard_requires_login(self):
        response = self.client.get(self.dashboard_url)
        self.assertNotEqual(response.status_code, 200)  


class UserModelTests(TestCase):
    def test_bio_field_optional(self):
        user = User.objects.create_user(username="bioUser", email="bio@example.com", password="pass123")
        self.assertIsNone(user.bio)

    def test_password_is_hashed_on_save(self):
        user = User(username="secure", email="secure@example.com")
        user.set_password("StrongPass123")
        user.save()
        self.assertNotEqual(user.password, "StrongPass123")  

    def test_check_password(self):
        user = User.objects.create_user(username="checkpass", email="check@example.com", password="StrongPass123")
        self.assertTrue(user.check_password("StrongPass123"))
        self.assertFalse(user.check_password("WrongPass"))
