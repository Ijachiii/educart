from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

from .models import *
from payment.sevis.models import SevisInformationUser
from support.consultation.models import Consultation
from .serializers import *
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from .utils import send_otp_signup, send_otp_password_reset, get_token_expiry_time
from educart_project.permissions import IsStaffOrReadOnly
from .custom_exception_handler import error_message

from django.utils import timezone

import re

import datetime
import random 

from django.contrib.auth import authenticate, login, logout

# Create your views here.

class UserSignUpView(APIView):
    serializer_class = UserSerializer
    CHOICES = [
        {"choice": "user"},
        {"choice": "consultant"},
    ]

    def get(self, request):
        return Response({
            "data": self.CHOICES,
            "message": "Success",
            "error": None
        }, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # errors_ = list(serializer.errors.values())[:len(serializer.errors)]
        # errors = []
        # for err in errors_:
        #     errors.append(err[0])

        return Response({
            "data": None,
            "errorMessage": error_message(serializer),
            "error": True
        }, status=status.HTTP_400_BAD_REQUEST)

        # return Response({
        #         "data": None,
        #         "errorMessage": serializer.errors,
        #         "error": True,
        #     }, status=status.HTTP_400_BAD_REQUEST)


class RegenerateOTPView(APIView):
    serializer_class = RegenerateOTPSerializer
    def post(self, request):
        serializer = RegenerateOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        id = serializer.validated_data["id"]

        try:
            user = CustomUser.objects.get(id=id)
        except CustomUser.DoesNotExist:
            return Response({
                "data": None,
                "errorMessage": [{
                    "code": "user_does_not_exist",
                    "message": "No user with this id"
                }],
                "error": True
            }, status=status.HTTP_404_NOT_FOUND)

        otp = random.randint(1000, 9999)
        otp_expiry = timezone.now() + datetime.timedelta(minutes=20)

        print(otp)

        user.otp = otp
        user.otp_expiry = otp_expiry
        user.otp_verified = False
        user.save()

        send_otp_signup(user.email, user.first_name, otp)
        return Response({
            "data": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "country_of_residence": user.country_of_residence,
                "country_code": user.country_code,
                "phone_number": user.phone_number
            },
            "message": "Successfully regenerated new otp",
            "error": False,
        }, status=status.HTTP_200_OK)
        

    
class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        if "email" in request.data:
            email = serializer.initial_data["email"]

            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return Response({
                    "data": None,
                    "errorMessage": [{
                        "code": "invalid_credentials",
                        "message": "No active account found with the given credentials"
                    }],
                    "error": True,
                }, status=status.HTTP_401_UNAUTHORIZED)
            
        if serializer.is_valid():
            user = serializer.user
            login(request, user)
            access_token_expiry = get_token_expiry_time(serializer.validated_data['access'])
            refresh_token_expiry = get_token_expiry_time(serializer.validated_data["refresh"])

            if not user.profile_picture:
                profile_picture = None
            else:
                profile_picture = user.profile_picture.url

            return Response({
                "data": {
                    "access": serializer.validated_data["access"],
                    "refresh": serializer.validated_data["refresh"],
                    "access_token_expiry": access_token_expiry,
                    "refresh_token_expiry": refresh_token_expiry,
                    "id": user.id,
                    "email": user.email,
                    "profile_picture": profile_picture,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "country_of_residence": user.country_of_residence,
                    "country_code": user.country_code,
                    "phone_number": user.phone_number,
                    "profile_completed": user.profile_completed,
                    "is_restricted": user.is_restricted,
                    "free_consultation": user.free_consultation
                },
                "message": "login successful",
                "error": False
            }, status=status.HTTP_200_OK)
        
        errors = []

        for err in serializer.errors:
            if serializer.errors[err][0] == "User not verified, OTP sent to email address":
                errors.append({
                    "code": "user_not_verified",
                    "message": serializer.errors[err][0]
                })
            else:
                errors = serializer.errors
        
        return Response({
                "data": {
                    "id": user.id,
                    "email": user.email,
                },
                "errorMessage": errors,
                "error": True,
            }, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = LogoutSerializer

    def get(self, request):
        return Response("Nonsese")

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():

            return Response({
                "data": None,
                "message": "Logout Successful",
                "error": False,
            }, status=status.HTTP_200_OK)
        
        errors = []
        
        for err in serializer.errors:
            errors.append({
            "code": "refresh_field",
            "message": str(serializer.errors[err][0])
        })
        
        return Response({
            "data": None,
            "errorMessage": errors,
            "error": True
        }, status=status.HTTP_400_BAD_REQUEST)

    

class ForgotPasswordView(APIView):
    serializer_class = ForgotPasswordSerializer
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({
                "data": None,
                "errorMessage": [{
                    "code": "user_does_not_exist",
                    "message": "No user found with this email address"
                }],
                "error": True,
            }, status=status.HTTP_404_NOT_FOUND)
        
        
        otp = random.randint(1000, 9999)
        user.otp = otp
        user.otp_expiry = timezone.now() + datetime.timedelta(minutes=20)
        user.save()

        send_otp_password_reset(email, user.first_name, otp)

        return Response({
                "data": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "country_of_residence": user.country_of_residence,
                    "country_code": user.country_code,
                    "phone_number": user.phone_number,
                },
                "message": f"an otp has been sent to {email}",
                "error": False,
            }, status=status.HTTP_200_OK)



class VerifyOTPView(APIView):
    serializer_class = VerifyOTPSerializer
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        print(serializer.initial_data)

        if serializer.is_valid():
            user = CustomUser.objects.filter(pk=serializer.validated_data["id"]).first()

            if not user:
                return Response({
                    "data": None,
                    "errorMessage": [{
                        "code": "user_does_not_exist",
                        "message": "Invalid user"
                    }],
                    "error": True,
                }, status=status.HTTP_404_NOT_FOUND)

            if (
                not user.is_verified
                and user.otp == request.data.get("otp") 
                and user.otp_expiry
                and timezone.now() < user.otp_expiry
            ): 
                user.is_verified = True
                user.otp_expiry = None
                user.otp = None
                user.otp_verified= True
                user.save()
                return Response({
                    "data": {
                        "id": user.id,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "country_of_residence": user.country_of_residence,
                        "country_code": user.country_code,
                        "phone_number": user.phone_number,
                    },
                    "message": "Successfully verified",
                    "error": False,
                }, status=status.HTTP_200_OK)

        
            otp = serializer.validated_data["otp"]

            if user.otp != otp or timezone.now() > user.otp_expiry:
                return Response({
                    "data": None,
                    "errorMessage": [{
                        "code": "invalid_otp",
                        "message": "Invalid OTP"
                    }],
                    "error": True,
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user.otp_expiry = None
            user.otp = None
            user.otp_verified= True
            user.save()

            return Response({
                    "data": None,
                    "message": "OTP verification Successful",
                    "error": False,
                }, status=status.HTTP_200_OK)
        
        return Response({
            "data": None,
            "errorMessage": error_message(serializer),
            "error": True
        }, status=status.HTTP_400_BAD_REQUEST)



class ResetPasswordView(APIView):
    serializer_class = ResetPasswordSerializer
    def put(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = CustomUser.objects.filter(pk=serializer.validated_data["id"]).first()
        if not user:
            return Response({
                "data": None,
                "errorMessage": [{
                    "code": "user_does_not_exist",
                    "message": "Invalid User"
                }],
                "error": True,
            }, status=status.HTTP_404_NOT_FOUND)
        
        password = serializer.validated_data["password"]
        confirm_password = serializer.validated_data["confirm_password"]

        errors_list = []

        if user.check_password(password):
            return Response({
                "data": None,
                "errorMessage": [{
                    "code": "weak_password",
                    "message": "New password and previous password should not be similar"
                }],
                "error": True,
            }, status=status.HTTP_400_BAD_REQUEST)
        
        elif len(password) < 8 or not re.search(r'\d', password):
            return Response({
                "data": None,
                "errorMessage": [{
                    "code": "weak_password",
                    "message": "Password must be at least 8 characters long and contain a numeric character."
                }],
                "error": True
            }, status=status.HTTP_400_BAD_REQUEST)

        elif password != confirm_password:
            return Response({
                "data": None,
                "errorMessage": [{
                    "code": "password_mismatch",
                    "message": "Passwords do not match"
                }],
                "error": True,
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(password)
        user.save()

        return Response({
                "data": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "country_of_residence": user.country_of_residence,
                    "country_code": user.country_code,
                    "phone_number": user.phone_number,
                },
                "message": "password reset successfully",
                "error": False,
            }, status=status.HTTP_200_OK)
    


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = ChangePasswordSerializer

    def put(self, request):
        user = self.request.user
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        old_password = serializer.validated_data["old_password"]
        new_password = serializer.validated_data["new_password"]
        confirm_password = serializer.validated_data["confirm_password"]

        if not user.check_password(old_password):
            return Response({
                "data": None,
                "errorMessage": [{
                    "code": "password_mismatch",
                    "message": "The current password you entered is incorrect"
                }],
                "error": True,
            }, status=status.HTTP_400_BAD_REQUEST)

        elif old_password == new_password:
            return Response({
                "data": None,
                "errorMessage": [{
                    "code": "weak_password",
                    "message": "new password should be different from old password"
                }],
                "error": True,
            }, status=status.HTTP_400_BAD_REQUEST)

        elif len(new_password) < 8 or not any(char.isdigit() for char in new_password):
            return Response({
                "data": None,
                "errorMessage": [{
                    "code": "weak_password",
                    "message": "Password must be at least 8 characters long and contain a numeric character."
                }],
                "error": True
            }, status=status.HTTP_400_BAD_REQUEST)

        elif new_password != confirm_password:
            return Response({
                "data": None,
                "errorMessage": [{
                    "code": "password_mismatch",
                    "message": "Passwords do not match"
                }],
                "error": True,
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()

        return Response({
                "data": None,
                "message": "Password updated successfully",
                "error": False,
            }, status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = ProfileSerializer

    def get(self, request):
        user = request.user
        if not user.profile_picture:
            profile_picture = None
        else:
            profile_picture = user.profile_picture.url

        if user.profile_picture and user.institution_of_study and  user.country_of_birth and user.state and user.city:
            user.profile_completed = True
            user.save()
        else:
            user.profile_completed = False
            user.save()
        
        return Response({
                "data": {
                    "id": user.id,
                    "user_type": user.user_type,
                    "profile_picture": profile_picture,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "country_code": user.country_code,
                    "phone_number": user.phone_number,
                    "country_of_residence": user.country_of_residence,
                    "institution_of_study": user.institution_of_study,
                    "country_of_birth": user.country_of_birth,
                    "city": user.city,
                    "state": user.state,
                    "profile_completed": user.profile_completed,
                    "is_restricted": user.is_restricted,                    
                    "free_consultation": user.free_consultation
                },
                "message": "success",
                "error": False,
            }, status=status.HTTP_200_OK)
    
    def patch(self, request):
        user = request.user
        serializer = ProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            if user.profile_picture and user.institution_of_study and user.country_of_birth and user.state and user.city:
                user.profile_completed = True
                user.save()
            
            if not user.profile_picture:
                profile_picture = None
            else:
                profile_picture = user.profile_picture.url
            
            return Response({
                "data": {
                    "id": user.id,
                    "user_type": user.user_type,
                    "profile_picture": profile_picture,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "country_code": user.country_code,
                    "phone_number": user.phone_number,
                    "country_of_residence": user.country_of_residence,
                    "institution_of_study": user.institution_of_study,
                    "country_of_birth": user.country_of_birth,
                    "city": user.city,
                    "state": user.state,
                    "profile_completed": user.profile_completed,
                    "is_restricted": user.is_restricted
                },
                "message": "profile updated successfully",
                "error": False,
            }, status=status.HTTP_200_OK)
        
        
        return Response({
            "data": None,
            "errorMessage": error_message(serializer),
            "error": True
        }, status=status.HTTP_400_BAD_REQUEST)



class OrderHistoryView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderHistorySerializer

    def get(self, request):
        user = request.user
        queryset = OrderHistory.objects.filter(user=user).order_by("-date")
        serializer = OrderHistorySerializer(queryset, many=True)
        return Response({
            "data": serializer.data,
            "message": "Successful",
            "error": None,
        }, status=status.HTTP_200_OK)



class TrackOrderView(APIView):
    permission_classes = [AllowAny,]
    serializer_class = TrackOrderSerializer

    def post(self, request):
        # user = request.user
        order_id = request.data.get("order_id")
        serializer = TrackOrderSerializer(data=request.data)

        if serializer.is_valid():
            queryset = OrderHistory.objects.filter(order_id=order_id).order_by('date')
            print(queryset)
            print(len(queryset))

            if len(queryset) < 1:
                queryset = OrderHistoryGuest.objects.filter(order_id=order_id).order_by('date')
                if len(queryset) < 1:
                    return Response({
                        "data": None,
                        "errorMessage": [{
                            "code": "invalid_order_id",
                            "message": "Order ID does not exist"
                        }],
                        "error": True 
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            query = OrderHistorySerializer(queryset, many=True)
            
            if "SEVIS Fee" in query.data[0]["order_type"]:
                type = "SEVIS Fee"
            elif "Consultation" in query.data[0]["order_type"]:
                type = "Consultation"
            else:
                type = None
            
            pending_payment = None
            confirmed_payment = None
            processing_order = None
            completed_order = None

            for order in query.data:
                if order["status"] == "Payment Pending":
                    pending_payment = order
                elif order["status"] == "Payment Confirmed":
                    confirmed_payment = order
                elif order["status"] == "Processing Order":
                    processing_order = order
                elif order["status"] == "Order Completed":
                    completed_order = order

            order_stage = [
                {
                    "stage": "Payment Pending",
                    "description": f"Your {type} payment order is yet to be received",
                    "date": pending_payment["date"],
                    "is_completed": True
                },
            ]

            if confirmed_payment:
                order2 = {
                    "stage": "Payment Confirmed",
                    "description": f"Your {type} payment order is confirmed successfully",
                    "date": confirmed_payment["date"],
                    "is_completed": True
                }
            else:
                order2 = {
                    "stage": "Payment Confirmed",
                    "description": f"Your {type} payment order is confirmed successfully",
                    "date": None,
                    "is_completed": False
                }
            order_stage.append(order2)

            if processing_order:
                order3 = {
                    "stage": "Processing Order",
                    "description": f"Your payment is on its way to the {type} government pocket",
                    "date": processing_order["date"],
                    "is_completed": True
                }
            else:
                order3 = {
                    "stage": "Processing Order",
                    "description": f"Your payment is on its way to the {type} government pocket",
                    "date": None,
                    "is_completed": False
                }
            order_stage.append(order3)

            if completed_order:
                order4 = {
                    "stage": "Order Completed",
                    "description": f"Your {type} payment order is completed",
                    "date": completed_order["date"],
                    "is_completed": True
                }
            else:
                order4 = {
                    "stage": "Order Completed",
                    "description": f"Your {type} payment order is completed",
                    "date": None,
                    "is_completed": False
                }
            order_stage.append(order4)

            most_recent = query.data[-1]
            data = [
                {
                    "order_id": most_recent["order_id"],
                    "order_type": most_recent["order_type"],
                    "amount": most_recent["amount"],
                    "status": most_recent["status"],
                    "order_stage": order_stage

                }
            ]
         
            return Response({
                "data": data,
                "message": "Success",
                "error": False
            }, status=status.HTTP_200_OK)
        
        return Response({
            "data": None,
            "errorMessage": error_message(serializer),
            "error": True
        }, status=status.HTTP_400_BAD_REQUEST)    


class OrderSummaryView(APIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = None

    def get(self, request, order_type):
        user = request.user

        if order_type == "sevis":
            try:
                # instance = SevisInformationUser.objects.get(user=user)
                instance = SevisInformationUser.objects.filter(user=user).latest("created_at")
            except SevisInformationUser.DoesNotExist:
                return Response({
                    "data": None,
                    "errorMessage": [{
                        "code": "sevis_does_not_exist",
                        "message": "sevis instance for this user does not exist"
                    }],
                    "error": True
                }, status=status.HTTP_404_NOT_FOUND)

            return Response({
                "data": {
                    "order_id": instance.order_id,
                    "order_type": f"SEVIS Fee/{instance.form_type}",
                    "sevis_fee": int(instance.sevis_fee),
                    "charges": 35,
                    "total_in_dollars": int(instance.fee_in_dollars),
                    "total_in_naira": int(instance.fee_in_naira),
                    "rate": 700
                },
                "message": "Success",
                "error": False
            })

        elif order_type == "consultation":
            try:
                instance = Consultation.objects.filter(user=user).latest("created_at")
            except Consultation.DoesNotExist:
                return Response({
                    "data": None,
                    "errorMessage": [{
                        "code": "consultation_does_not_exist",
                        "message": "consultation instance for this user does not exist"
                    }],
                    "error": True
                }, status=status.HTTP_404_NOT_FOUND)

            return Response({
                "data": {
                    "order_id": instance.order_id,
                    "order_type": "Consultation",
                    "consultation_fee": instance.consultation_fee,
                    "charges": 35,
                    "total": instance.fee_in_dollars,
                    "total_in_naira": instance.fee_in_naira,
                    "rate": 700
                },
                "message": "Success",
                "error": False
            })
        
        else:
            return Response({
                "data": None,
                "errorMessage": [{
                    "code": "invalid_order_type",
                    "message": "Invalid order type"
                }],
                "error": True
            }, status=status.HTTP_400_BAD_REQUEST)
        


class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny,]
    serializer_class = None

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        access_token_expiry = get_token_expiry_time(response.data["access"])
        refresh_token_expiry = get_token_expiry_time(response.data["refresh"])
        response.data["access_token_expiry"] = access_token_expiry
        response.data["refresh_token_expiry"] = refresh_token_expiry
        
        return Response({
            "data": response.data,
            "message": "Success",
            "error": False
        }, status=status.HTTP_200_OK)



class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = None

    def post(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response({
            "data": None,
            "message": "user deleted!",
            "error": False,
        }, status=status.HTTP_200_OK)   




# class TokenExpirationView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = TimeSerializer(data=request.data)
#         print(datetime.datetime.utcnow().timestamp())
#         print(timezone.now().timestamp())
#         print("bro")

#         if serializer.is_valid():
#             try:
#                 # Get the encoded token from the request header
#                 encoded_token = serializer.validated_data["access"]
#                 print(encoded_token)
#                 decoded_token = jwt.decode(encoded_token, SECRET_KEY, algorithms=['HS256'])
#                 print(decoded_token)
#                 expiration_timestamp = decoded_token['exp']
#                 print(expiration_timestamp)

#                 # Calculate the time left for the token to expire
#                 current_timestamp = datetime.datetime.utcnow().timestamp() + 3600
#                 print(current_timestamp)
#                 time_left = expiration_timestamp - current_timestamp
#                 print(time_left)

#                 return Response({'time_left_to_expire': time_left}, status=status.HTTP_200_OK)
#             except Exception as e:
#                 return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
#         return Response(serializer.errors)


    # def post(self, request, *args, **kwargs):
    #     serializer = TimeSerializer(data=request.data)
    #     print(SIMPLE_JWT)
        
    #     if serializer.is_valid():
    #         accesstoken = serializer.validated_data["access"]
    #         print(accesstoken)

    #         token = RefreshToken(accesstoken)
    #         payload = token.payload
    #         print("yayyy")
    #         print(payload)

    #         expiration_timestamp = payload("exp")
    #         current_timestamp = datetime.utcnow().timestamp()

    #         time_left = expiration_timestamp - current_timestamp
            
    #         print(expiration_timestamp)
    #         print(current_timestamp)
    #         print(time_left)

    #         return Response("What's UP!!!")
        
    #     return Response(serializer.errors)


        

# class AddressBookView(APIView):
#     permission_classes = [IsAuthenticated,]
#     serializer_class = AddressBookSerializer

#     def get(self, request):
#         user = request.user
#         instance = AddressBook.objects.filter(user=user)
#         serializer = AddressBookSerializer(instance, many=True)

#         user_address = AddressBook.objects.filter(user=user).exists()
#         if user.profile_picture and user.institution_of_study and user_address:
#             user.profile_completed = True
#             user.save()

#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         user = request.user
#         serializer = AddressBookSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()

#             user_address = AddressBook.objects.filter(user=user).exists()
#             if user.profile_picture and user.institution_of_study and user_address:
#                 user.profile_completed = True
#                 user.save()

#             return Response({
#                 "data": serializer.data,
#                 "message": "",
#                 "error": "False"
#             })
        
        
#         errors = []
        
#         for err in serializer.errors:
#             errors.append({
#             "code": f"empty_{err}_field",
#             "message": str(serializer.errors[err][0])
#         })
        
#         return Response({
#             "data": None,
#             "errorMessage": errors,
#             "error": True
#         }, status=status.HTTP_400_BAD_REQUEST)
        


#profile_picture = request.data.get("profile_picture", None)

        # if profile_picture is None:
        #     try:
        #         user.profile_picture = user.profile_picture
        #     except ValueError:
        #         serializer = ProfileSerializer(user, data=request.data, partial=True)
        #         serializer.save()
        #         if not user.profile_picture:
        #             profile_picture = None
        #         else:
        #             profile_picture = user.profile_picture.url
        #         return Response({
        #             "data": {
        #                 "id": user.id,
        #                 "profile_picture": profile_picture,
        #                 "first_name": user.first_name,
        #                 "last_name": user.last_name,
        #                 "email": user.email,
        #                 "country_code": user.country_code,
        #                 "phone_number": user.phone_number,
        #                 "country_of_residence": user.country_of_residence,
        #                 "institution_of_study": user.institution_of_study,
        #                 "profile_completed": user.profile_completed,
        #                 "is_restricted": user.is_restricted
        #             },
        #             "message": "profile updated successfully",
        #             "error": False,
        #         }, status=status.HTTP_200_OK)
        # else:
        #     # Manually update the profile_picture field without triggering validation
        #     setattr(user, 'profile_picture', profile_picture)





# class CreatePinView(APIView):
#     permission_classes = [IsAuthenticated,]
#     serializer_class = CreateTransactionPinSerializer

#     def get(self, request, format=None):
#         security_questions = SecurityQuestions.objects.all()
#         serializer = SecurityQuestionSerializer(security_questions, many=True)
#         return Response({
#                 "data": serializer.data,
#                 "message": None,
#                 "error": False,
#             }, status=status.HTTP_200_OK)

#     def post(self, request):
#         serializer = CreateTransactionPinSerializer(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({
#                 "data": None,
#                 "message": "Transaction pin successfully created",
#                 "error": False,
#             }, status=status.HTTP_200_OK)


# class ChangeTransactionPinView(APIView):
#     permission_classes = [IsAuthenticated,]
#     serializer_class = ChangeTransactionPinSerializer

#     def put(self, request):
#         user = self.request.user
#         serializer = ChangeTransactionPinSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         old_pin = base64.b64encode(bytes(serializer.validated_data["old_pin"], "utf-8"))
#         new_pin = base64.b64encode(bytes(serializer.validated_data["new_pin"], "utf-8"))
#         confirm_pin = base64.b64encode(bytes(serializer.validated_data["confirm_pin"], "utf-8"))
#         print(str(old_pin))
#         print(str(user.transaction_pin))

#         if str(user.transaction_pin) != str(old_pin):
#             return Response({
#                 "data": None,
#                 "errorMessage": [{
#                     "code": "pin_mismatch",
#                     "message": "The current pin you entered is incorrect"
#                 }],
#                 "error": True,
#             }, status=status.HTTP_401_UNAUTHORIZED)
        
#         elif old_pin == new_pin:
#             return Response({
#                 "data": None,
#                 "message": "new pin should be different from old pin",
#                 "errorMessage": [{
#                     "code": "weak_pin",
#                     "message": "new pin should be different from old pin"
#                 }],
#                 "error": True,
#             }, status=status.HTTP_401_UNAUTHORIZED)
        
#         elif new_pin != confirm_pin:
#             return Response({
#                 "data": None,
#                 "errorMessage": [{
#                     "code": "pin_mismatch",
#                     "message": "Pins do not match"
#                 }],
#                 "error": True,
#             }, status=status.HTTP_401_UNAUTHORIZED)
        
#         user.pin = new_pin
#         user.save()

#         return Response({
#                 "data": None,
#                 "message": "Pin updated successfully",
#                 "error": False,
#             }, status=status.HTTP_200_OK)
#         # return Response({"detail": "Pin updated successfully"}, status=status.HTTP_200_OK)


# class SecurityQuestionView(APIView):
#     permission_classes = [IsAuthenticated,]
#     serializer_class = SecurityAnswerSerializer
#     def get(self, request, format=None):
#         user = request.user
#         serializer = SecurityAnswerSerializer(user)
#         return Response({
#                 "data": serializer.data,
#                 "message": None,
#                 "error": False,
#             }, status=status.HTTP_200_OK)
#         # return Response(serializer.data, status=status.HTTP_200_OK)

    
#     def post(self, request):
#         user = self.request.user
#         serializer = SecurityAnswerSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         security_answer_1 = serializer.validated_data["security_answer_1"]
#         security_answer_2 = serializer.validated_data["security_answer_2"]
#         security_answer_3 = serializer.validated_data["security_answer_3"]

#         errors = []

#         if security_answer_1.lower() != user.security_answer_1.lower():
#             # error1 = {"code": "invalid_answer", "message": "incorrect answer to security question" }
#             # errors.append(error1)
#             return Response({
#                 "data": None,
#                 "errorMessage": [{
#                     "code": "invalid_answer",
#                     "message": "incorrect answer to security question"
#                 }],
#                 "error": True,
#             }, status=status.HTTP_401_UNAUTHORIZED)
#             # return Response({"detail": "First Answer is incorrect"}, status=status.HTTP_401_UNAUTHORIZED)
        
#         if security_answer_2.lower() != user.security_answer_2.lower():
#             # error2 = {"code": "invalid_answer", "message": "incorrect answer to security question" }
#             # errors.append(error2)
#             return Response({
#                 "data": None,
#                 "errorMessage": [{
#                     "code": "invalid_answer",
#                     "message": "incorrect answer to security question"
#                 }],
#                 "error": True,
#             }, status=status.HTTP_401_UNAUTHORIZED)
#             # return Response({"detail": "Second Answer is incorrect"}, status=status.HTTP_401_UNAUTHORIZED)
        
#         if security_answer_3.lower() != user.security_answer_3.lower():
#             error3 = {"code": "invalid_answer", "message": "incorrect answer to security question" }
#             errors.append(error3)
#             return Response({
#                 "data": None,
#                 "errorMessage": [{
#                     "code": "invalid_answer",
#                     "message": "incorrect answer to security question"
#                 }],
#                 "error": True,
#             }, status=status.HTTP_401_UNAUTHORIZED)
#             # return Response({"detail": "Third Answer is incorrect"}, status=status.HTTP_401_UNAUTHORIZED)
        
#         otp = random.randint(1000, 9999)
#         user.otp = otp
#         user.otp_expiry = timezone.now() + datetime.timedelta(minutes=20)
#         user.save()

#         send_otp_pin_reset(user.email, user.first_name, otp)
        
#         return Response({
#                 "data": None,
#                 "message": "otp sent to your email",
#                 "error": False,
#             }, status=status.HTTP_200_OK)
    


# class VerifyPinChangeOTPView(APIView):
#     permission_classes = [IsAuthenticated,]
#     serializer_class = VerifyOTPSerializer
#     def post(self, request):
#         user = request.user
#         if (
#             user.otp == request.data.get("otp") 
#             and user.otp_expiry
#             and timezone.now() < user.otp_expiry
#         ): 
#             user.otp_expiry = None
#             user.otp = None
#             user.save()

#             return Response({
#                 "data": None,
#                 "message": "successfully verified",
#                 "error": False,
#             }, status=status.HTTP_200_OK)

#         serializer = VerifyOTPSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         otp = serializer.validated_data["otp"]

#         if user.otp != otp:
#             return Response({
#                 "data": None,
#                 "errorMessage": [{
#                     "code": "invalid_otp",
#                     "message": "Invalid OTP"
#                 }],
#                 "error": True,
#             }, status=status.HTTP_400_BAD_REQUEST)
#             # return Response({"detail": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        
#         return Response({
#                 "data": None,
#                 "message": "otp verification successful",
#                 "error": False,
#             }, status=status.HTTP_200_OK)
#         # return Response({"detail": "OTP Verifification Successful"}, status=status.HTTP_200_OK)
    

# """This view is to reset transaction pins that has been forgotten"""
# class ResetTransactionPinView(APIView):
#     permission_classes = [IsAuthenticated,]
#     serializer_class = ResetTransactionPinSerializer

#     def put(self, request):
#         user = self.request.user
#         serializer = ResetTransactionPinSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         new_pin = base64.b64encode(bytes(serializer.validated_data["new_pin"], "utf-8"))
#         confirm_pin = base64.b64encode(bytes(serializer.validated_data["confirm_pin"], "utf-8"))

#         if new_pin != confirm_pin:
#             return Response({
#                 "data": None,
#                 "errorMessage": [{
#                     "code": "pin_mismatch",
#                     "message": "Pins do not match"
#                 }],
#                 "error": True,
#             }, status=status.HTTP_401_UNAUTHORIZED)
        
#         user.pin = new_pin

#         user.save()

#         return Response({
#                 "data": None,
#                 "message": "Pin updated successfully",
#                 "error": False,
#             }, status=status.HTTP_200_OK)
#         # return Response({"detail": "Pin updated successfully"}, status=status.HTTP_200_OK)




# class TrackOrderView(APIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = TrackOrderSerializer

#     def post(self, request):
#         user = request.user
#         order_id = request.data.get("order_id")
#         serializer = TrackOrderSerializer(data=request.data)

#         if serializer.is_valid():
#             queryset = OrderHistory.objects.filter(user=user, order_id=order_id).order_by('date')
#             query = OrderHistorySerializer(queryset, many=True)

#             if len(query.data) < 1:
#                 return Response({
#                     "data": None,
#                     "errorMessage": [{
#                         "code": "invalid_order_id",
#                         "message": "Order ID does not exist"
#                     }],
#                     "error": True 
#                 }, status=status.HTTP_400_BAD_REQUEST)
            
#             if "SEVIS Fee" in query.data[0]["order_type"]:
#                 type = "SEVIS Fee"
#             elif "Consultation" in query.data[0]["order_type"]:
#                 type = "Consultation"
#             else:
#                 type = None
            
#             pending_payment = None
#             confirmed_payment = None
#             processing_order = None
#             completed_order = None

#             for order in query.data:
#                 if order["status"] == "Payment Pending":
#                     pending_payment = order
#                 elif order["status"] == "Payment Confirmed":
#                     confirmed_payment = order
#                 elif order["status"] == "Processing Order":
#                     processing_order = order
#                 elif order["status"] == "Order Completed":
#                     completed_order = order

#             order_stage = [
#                 {
#                     "stage": "Payment Pending",
#                     "description": f"Your {type} payment order is yet to be received",
#                     "date": pending_payment["date"],
#                     "is_completed": True
#                 },
#             ]

#             if confirmed_payment:
#                 order2 = {
#                     "stage": "Payment Confirmed",
#                     "description": f"Your {type} payment order is confirmed successfully",
#                     "date": confirmed_payment["date"],
#                     "is_completed": True
#                 }
#             else:
#                 order2 = {
#                     "stage": "Payment Confirmed",
#                     "description": f"Your {type} payment order is confirmed successfully",
#                     "date": None,
#                     "is_completed": False
#                 }
#             order_stage.append(order2)

#             if processing_order:
#                 order3 = {
#                     "stage": "Processing Order",
#                     "description": f"Your payment is on its way to the {type} government pocket",
#                     "date": processing_order["date"],
#                     "is_completed": True
#                 }
#             else:
#                 order3 = {
#                     "stage": "Processing Order",
#                     "description": f"Your payment is on its way to the {type} government pocket",
#                     "date": None,
#                     "is_completed": False
#                 }
#             order_stage.append(order3)

#             if completed_order:
#                 order4 = {
#                     "stage": "Order Completed",
#                     "description": f"Your {type} payment order is completed",
#                     "date": completed_order["date"],
#                     "is_completed": True
#                 }
#             else:
#                 order4 = {
#                     "stage": "Order Completed",
#                     "description": f"Your {type} payment order is completed",
#                     "date": None,
#                     "is_completed": False
#                 }
#             order_stage.append(order4)

#             most_recent = query.data[-1]
#             data = [
#                 {
#                     "id": most_recent["id"],
#                     "order_id": most_recent["order_id"],
#                     "order_type": most_recent["order_type"],
#                     "amount": most_recent["amount"],
#                     "status": most_recent["status"],
#                     "user": most_recent["user"],
#                     "order_stage": order_stage

#                 }
#             ]
         
#             return Response({
#                 "data": data,
#                 "message": "Success",
#                 "error": False
#             }, status=status.HTTP_200_OK)
        
#         errors = []
        
#         for err in serializer.errors:
#             errors.append({
#             "code": f"{err}_field",
#             "message": str(serializer.errors[err][0])
#         })
        
#         return Response({
#             "data": None,
#             "errorMessage": errors,
#             "error": True
#         }, status=status.HTTP_400_BAD_REQUEST)



# class TrackOrderGuestView(APIView):
#     permission_classes = [AllowAny]
#     serializer_class = TrackOrderSerializer

#     def post(self, request):
#         order_id = request.data.get("order_id")
#         serializer = TrackOrderSerializer(data=request.data)

#         if serializer.is_valid():
#             queryset = OrderHistoryGuest.objects.filter(order_id=order_id)
#             query = OrderHistoryGuestSerializer(queryset, many=True)

#             return Response({
#                 "data": query.data,
#                 "message": "Successful",
#                 "error": False
#             }, status=status.HTTP_200_OK)
        

#         errors = []
        
#         for err in serializer.errors:
#             errors.append({
#             "code": f"{err}_field",
#             "message": str(serializer.errors[err][0])
#         })
        
#         return Response({
#             "data": None,
#             "errorMessage": errors,
#             "error": True
#         }, status=status.HTTP_400_BAD_REQUEST)