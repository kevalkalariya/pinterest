import pytest
from django.test import TestCase, Client
from django.urls import reverse
from users.models import Profile
from pytest_django.asserts import assertTemplateUsed, assertRedirects


class RegisterCustomerTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {'email': 'bhargav1@gmail.com', 'password1': '123456@As', 'password2': '123456@As'}
        self.user_invalid_email_data = {'email': ['bhargav'], 'password1': ['123456@As'], 'password2': ['123456@As']}
        self.user_missmatch_password_data = {'email': ['bhargav1@gmail.com'], 'password1': ['123456@A'],
                                             'password2': ['123456@As']}
        self.user_invalid_password_data = {'email': ['bhargav1@gmail.com'], 'password1': ['123456As'],
                                           'password2': ['123456As']}
        register_url = self.client.get(reverse('register'))

    def test_register_user_get_request(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_user_valid_data(self):
        response = self.client.post(reverse('register'), self.user_data, format='text/html')
        self.assertEqual(response.url, reverse('interest'))
        self.assertEqual(response.status_code, 302)

    def test_register_customer_invalid_email_data(self):
        response = self.client.post(reverse('register'), self.user_invalid_email_data, format='text/html')
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertEqual(response.status_code, 200)

    def test_register_customer_missmatch_password_data(self):
        response = self.client.post(reverse('register'), self.user_missmatch_password_data, format='text/html')
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertEqual(response.status_code, 200)

    def test_register_customer_invalid_password_data(self):
        response = self.client.post(reverse('register'), self.user_invalid_password_data, format='text/html')
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertEqual(response.status_code, 200)


class LogoutTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_logout_user(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)


class TestProfile:
    @pytest.mark.django_db
    def test_get_profile(self, create_profile, client):
        p = create_profile()
        client.login(email=p.user.email, password='Testing321@')
        response = client.get(reverse('profile'))
        assert response.status_code == 200
        assertTemplateUsed(response, 'users/profile.html')

    def test_post_profile(self, create_profile, client):
        p = create_profile()

        client.login(email=p.user.email, password='Testing321@')
        response = client.post(reverse('profile'), {'firstname': 'Hetvee'})
        assert response.status_code == 302


class TestViewProfile:
    @pytest.mark.django_db
    def test_viewprofile(self, create_profile, client):
        p = create_profile()
        user = client.login(email=p.user.email, password='Testing321@')
        response = client.get(reverse('view-profile'))
        assert response.status_code == 200
        assertTemplateUsed(response, 'users/view_profile.html')
