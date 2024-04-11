"""
Tests for the user api
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')

def create_user(**params):
    """Create and return new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public(unauthenticated request(like register user)) features of the user API"""

    def setUp(self):
        """Automatic create user for test"""
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creatin a user is successfull"""
        payload = {
            'email':'test@example.com',
            'password':'testpass123',
            'name':'Test Name',
        }
        """Make HTTP post request to our CREATE_USER_URL and passin a payload"""

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        """Check if password is not in the responce data"""
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Test erroe returned if user ith email exists"""
        payload = {
            'email':'test@example.com',
            'password':'testpass123',
            'name':'Test Name',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars"""
        payload = {
            'email':'test@example.com',
            'password':'pw',
            'name':'Test Name',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model.objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)