from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

# Create your tests here.
class CountriesApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_countries(self):
        url = "/api/v1/countries/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
