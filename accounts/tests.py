from django.test import TestCase
from rest_framework.test import APIClient, APIRequestFactory
from .models import *
from rest_framework import status
import json

# Create your tests here.
class AccountsModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            user_type="user",
            email="davidaudu1010@gmail.com",
            first_name = "David",
            last_name = "Audu",
            country_of_residence = "Nigeria",
            country_of_birth = "Nigeria",
            institution_of_study = "Unilag",
            phone_number = "08126827413",
            country_code = 234,
            # profile_picture = SimpleUploadedFile("/Dave.jpg", b"file_content", content_type="image/jpeg"),
            city = "Yaba",
            state = "Lagos"
        )

        self.consultant = Consultant.objects.create(
            user = self.user,
            name = "David Audu",
            price_per_hour = 10,
            specialization = "FAQs",
            qualification = "Software Engineering",
            bio = "Dedicated",
            years_of_experience = 5,
            state = "Lagos",
            country = "Nigeria"
        )

        self.orderhistory = OrderHistory.objects.create(
            user = self.user,
            order_id = "SECNEKWK10",
            order_type = "sevis",
            amount = 2000100,
            status = "Payment Pending"
        )

        self.orderhistoryguest = OrderHistoryGuest.objects.create(
            order_id = "SECNEKWK10",
            order_type = "sevis",
            amount = 2000100,
            status = "Payment Pending"
        )

    def test_user_model_content(self):
        self.assertEqual(self.user.user_type, "user")
        self.assertEqual(self.user.email, "davidaudu1010@gmail.com")
        self.assertEqual(self.user.first_name, "David")
        self.assertEqual(self.user.last_name, "Audu")
        self.assertEqual(self.user.country_of_residence, "Nigeria")
        self.assertEqual(self.user.country_of_birth, "Nigeria")
        self.assertEqual(self.user.institution_of_study, "Unilag")
        self.assertEqual(self.user.phone_number, "08126827413")
        self.assertEqual(self.user.country_code, 234)
        self.assertEqual(self.user.city, "Yaba")
        self.assertEqual(self.user.state, "Lagos")
        # self.assertEqual(self.user.profile_picture.name, "profile_picture/David.jpg")


    def test_consultant_model(self):
        self.assertEqual(self.consultant.user, self.user)
        self.assertEqual(self.consultant.name, "David Audu")
        self.assertEqual(self.consultant.price_per_hour, 10)
        self.assertEqual(self.consultant.specialization, "FAQs")
        self.assertEqual(self.consultant.qualification, "Software Engineering")
        self.assertEqual(self.consultant.state, "Lagos")
        self.assertEqual(self.consultant.country, "Nigeria")
        self.assertEqual(self.consultant.years_of_experience, 5)
        self.assertEqual(self.consultant.bio, "Dedicated")


    def test_orderhistory_model_content(self):
        self.assertEqual(self.orderhistory.user, self.user)
        self.assertEqual(self.orderhistory.order_id, "SECNEKWK10")
        self.assertEqual(self.orderhistory.order_type, "sevis")
        self.assertEqual(self.orderhistory.amount, 2000100)
        self.assertEqual(self.orderhistory.status, "Payment Pending")
        self.assertIsNotNone(self.orderhistory.date)


    def test_orderhistoryguest_model_content(self):
        self.assertEqual(self.orderhistoryguest.order_id, "SECNEKWK10")
        self.assertEqual(self.orderhistoryguest.order_type, "sevis")
        self.assertEqual(self.orderhistoryguest.amount, 2000100)
        self.assertEqual(self.orderhistoryguest.status, "Payment Pending")
        self.assertIsNotNone(self.orderhistoryguest.date)


class AccountsRequestTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email="test@email.com", password="donietello", is_verified=True)
        self.client = APIClient()
        url = "/api/v1/auth/login/"
        data = {"email": "test@email.com", "password": "donietello"}
        response = self.client.post(url, data, format='json')
        self.token = response.data["data"]["access"]


    def test_login(self):
        url = "/api/v1/auth/login/"
        data = {"email": "test@email.com", "password": "donietello"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data["data"])


    def test_get_profile_view(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        url = "/api/v1/account-setup/profile/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    def test_patch_profile_view(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        url = "/api/v1/account-setup/profile/"
        data = {
            "first_name": "David",
            "last_name": "Audu",
            "country_code": 234,
            "phone_number": "8126827413",
            "country_of_residence": "Nigeria",
            "institution_of_study": "Unilag",
            "country_of_birth": "Nigeria",
            "state": "Lagos",
            "city": "Yaba"
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("David", response.data["data"].values())
        self.assertIn("Audu", response.data["data"].values())
        self.assertIn(234, response.data["data"].values())
        self.assertIn("8126827413", response.data["data"].values())
        self.assertIn("Nigeria", response.data["data"].values())
        self.assertIn("Unilag", response.data["data"].values())
        self.assertIn("Nigeria", response.data["data"].values())
        self.assertIn("Lagos", response.data["data"].values())
        self.assertIn("Yaba", response.data["data"].values())


    def test_get_orderhistory(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        url = "/api/v1/dashboard/order-history/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

