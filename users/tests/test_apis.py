# tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class HelloAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_hello_api(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': '歡迎來到 EatHub API'})


class UserAuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.base_url = '/api/v1/auth'

    def test_get_csrf_token(self):
        response = self.client.get(f'{self.base_url}/csrf')
        self.assertEqual(response.status_code, 200)
        self.assertIn('csrftoken', response.cookies)

    def test_signup(self):
        data = {
            'firstName': 'testuser',
            'lastName': 'testuser',
            'userName': 'testuser',
            'email': 'testuser@example.com',
            'password': 'strong_password123'
        }
        response = self.client.post(f'{self.base_url}/signup', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('user', response.data)

    def test_login(self):
        data = {
            'firstName': 'testuser',
            'lastName': 'testuser',
            'userName': 'testuser',
            'email': 'testuser@example.com',
            'password': 'strong_password123'
        }
        self.client.post(f'{self.base_url}/signup', data, format='json')

        login_data = {
            'email': 'testuser@example.com',
            'password': 'strong_password123'
        }
        response = self.client.post(f'{self.base_url}/login', login_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('user', response.data)

    def test_me_requires_auth(self):
        data = {
            'firstName': 'testuser',
            'lastName': 'testuser',
            'userName': 'testuser',
            'email': 'testuser@example.com',
            'password': 'strong_password123'
        }
        self.client.post(f'{self.base_url}/signup', data, format='json')
        login_data = {
            'email': 'testuser@example.com',
            'password': 'strong_password123'
        }
        self.client.post(f'{self.base_url}/login', login_data, format='json')

        resp = self.client.get(f'{self.base_url}/me')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['userName'], 'testuser')

    def test_logout(self):
        data = {
            'firstName': 'testuser',
            'lastName': 'testuser',
            'userName': 'testuser',
            'email': 'testuser@example.com',
            'password': 'strong_password123'
        }
        self.client.post(f'{self.base_url}/signup', data, format='json')
        login_data = {
            'email': 'testuser@example.com',
            'password': 'strong_password123'
        }
        self.client.post(f'{self.base_url}/login', login_data, format='json')

        response = self.client.post(f'{self.base_url}/logout')
        self.assertEqual(response.status_code, 200)
