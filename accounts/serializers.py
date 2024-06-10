import datetime
from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.utils import timezone
import random
from django.conf import settings
from rest_framework import serializers
from .models import *
from .utils import send_otp_signup, send_otp_login
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import random
import string
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from django.contrib.auth import authenticate

from .diposable_emails import disposable_mails
from .validators import validate_password_complexity

letters = string.ascii_lowercase


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def validate_password(self, value):
        try:
            validate_password_complexity(value)
        except ValidationError as e:
            # Raise a custom validation error with a custom error message
            raise serializers.ValidationError("Password must be at least 8 characters long and contain a numeric character.")

        return value


    class Meta:
        model = CustomUser
        fields = ("id", "user_type", "email", "first_name", "last_name", "country_of_residence", "country_code", "phone_number", "password")


    def to_representation(self, instance):
        instance = super().to_representation(instance)
        # modify the response data as needed
        return {
            "data": instance,
            "message": {
                "success": [f"User created successfully. OTP sent to {instance['email']}"]
            },
            "error": False
        }
    
    def create(self, validated_data):
        otp = random.randint(1000, 9999)
        otp_expiry = timezone.now() + datetime.timedelta(minutes=20)
        num = random.randint(10000000, 99999999)
        wrd = "".join(random.choice(letters) for i in range(2))
        wallet_id = str(num)+wrd
        print(wallet_id)
        user = CustomUser(
            user_type=validated_data["user_type"],
            email=validated_data["email"],
            first_name = validated_data["first_name"],
            last_name = validated_data["last_name"],
            country_of_residence = validated_data["country_of_residence"],
            country_code = validated_data["country_code"],
            phone_number = validated_data["phone_number"],
            wallet_id = wallet_id,
            otp = otp,
            otp_expiry = otp_expiry
        )

        user.set_password(validated_data["password"]) 
        user.save()

        send_otp_signup(validated_data["email"], validated_data["first_name"], otp)

        return user


class RegenerateOTPSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    id = serializers.CharField()
    password = serializers.CharField(min_length=8, write_only=True, required=True)
    confirm_password = serializers.CharField(min_length=8, write_only=True, required=True)


class VerifyOTPSerializer(serializers.Serializer):
    id = serializers.CharField()
    otp = serializers.CharField(max_length=4)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        if not user.is_verified:
            otp = random.randint(1000, 9999)
            otp_expiry = timezone.now() + datetime.timedelta(minutes=20)
            user.otp = otp
            user.otp_expiry = otp_expiry
            send_otp_login(user.email, user.first_name, otp)
            user.save()
            raise serializers.ValidationError("User not verified, OTP sent to email address")
        return data
    

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            raise ValidationError("Token is blacklisted")
        return attrs

    # def save(self, **kwargs):
    #     #RefreshToken(self.token).blacklist()
    #     try:
    #         RefreshToken(self.token).blacklist()
    #     except TokenError:
    #         raise ValidationError("Token has been blacklisted")
    

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("profile_picture", "first_name", "last_name", "country_code", "phone_number", "country_of_residence", "institution_of_study", "country_of_birth", "state", "city")


class OrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderHistory
        exclude = ("user",)


class TrackOrderSerializer(serializers.Serializer):
    order_id = serializers.CharField(required=True)


# class TimeSerializer(serializers.Serializer):
#     access = serializers.CharField(required=True)


# class OrderHistoryGuestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderHistoryGuest
#         fields = "__all__"


# class AddressBookSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AddressBook
#         fields = "__all__"
#         extra_kwargs = {
#             "home_address": {"error_messages": {"required": "Home address field is required"}},
#             "city": {"error_messages": {"required": "City field is required"}},
#             "country": {"error_messages": {"required": "Country field is required"}},
#         }



# class CreateTransactionPinSerializer(serializers.Serializer):
#     transaction_pin = serializers.CharField(max_length=4, required=True)
#     confirm_transaction_pin = serializers.CharField(max_length=4, required=True)
#     def validate(self, data):
#         if data["transaction_pin"] != data["confirm_transaction_pin"]:
#             raise serializers.ValidationError("Pins do not match") 
#         return data

#     def create(self, validated_data):
#         user = self.context["request"].user

#         user.transaction_pin = validated_data["transaction_pin"]
#         user.security_question_1 = validated_data["security_question_1"]
#         user.security_answer_1 = validated_data["security_answer_1"]
#         user.security_question_2 = validated_data["security_question_2"]
#         user.security_answer_2 = validated_data["security_answer_2"]
#         user.security_question_3 = validated_data["security_question_3"]
#         user.security_answer_3 = validated_data["security_answer_3"]
#         user.save()

#         return user
    

# class ChangeTransactionPinSerializer(serializers.Serializer):
#     old_pin = serializers.CharField(required=True)
#     new_pin = serializers.CharField(required=True)
#     confirm_pin = serializers.CharField(required=True)



# class SecurityQuestionSerializer(serializers.Serializer):
#     """
#     Serializer for MyModel model
#     """

#     # Define a custom SerializerMethodField to extract and return each value
#     security_question = serializers.SerializerMethodField()

#     def get_security_question(self, obj):
#         """
#         Custom method to extract and return each value
#         """
#         # Split the values field by commas and return as a list
#         return obj.id, obj.security_question


# class SecurityAnswerSerializer(serializers.ModelSerializer):
#     security_answer_1 = serializers.CharField(max_length=255)
#     security_answer_2 = serializers.CharField(max_length=255)
#     security_answer_3 = serializers.CharField(max_length=255)

#     class Meta:
#         model = CustomUser
#         fields = ("security_question_1", "security_answer_1", "security_question_2", "security_answer_2", "security_question_3", "security_answer_3",)


# class ResetTransactionPinSerializer(serializers.Serializer):
#     new_pin = serializers.CharField(max_length=4, required=True)
#     confirm_pin = serializers.CharField(max_length=4, required=True)