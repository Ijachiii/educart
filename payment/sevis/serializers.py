from rest_framework import serializers
from .models import *


class SevisInformationPage1Serializer(serializers.ModelSerializer):

    class Meta:
        model = SevisInformationUser
        fields = ("user", "sevis_id", "last_name", "given_name", "date_of_birth", "form", "passport", "international_passport")
        extra_kwargs = {
            "sevis_id": {"error_messages": {"required": "Sevis id field is required"}},
            "last_name": {"error_messages": {"required": "Last name field is required"}},
            "given_name": {"error_messages": {"required": "Given Name field is required"}},
            "date_of_birth": {"error_messages": {"required": "Date of birth field is required"}},
            "form": {"error_messages": {"required": "Form field requires a file to be submitted"}},
            "passport": {"error_messages": {"required": "Passport field requires a file to be submitted"}},
            "international_passport": {"error_messages": {"required": "International Passport field requires a file to be submitted"}},
        }
    

class SevisInformationPage2Serializer(serializers.ModelSerializer):

    class Meta:
        model = SevisInformationUser
        fields =("form_type", "category", "email", "phone_number", "country_of_citizenship", "country_of_birth")
        extra_kwargs = {
            "form_type": {"error_messages": {"required": "Form type field is required"}},
            "I_20_email": {"error_messages": {"required": "Email field is required"}},
            "I_20_phone_number": {"error_messages": {"required": "Phone number field is required"}},
            "I_20_country_of_citizenship": {"error_messages": {"required": "Country of citizenship field is required"}},
            "I_20_country_of_birth": {"error_messages": {"required": "Country of birth field is required"}},
        }


class SevisInformationPage3Serializer(serializers.ModelSerializer):

    class Meta:
        model = SevisInformationUser
        fields = ("street_address_1", "street_address_2", "country", "state", "city")
        extra_kwargs = {
            "street_address_1": {"error_messages": {"required": "Street address 1 field is required"}},
            "street_address_2": {"error_messages": {"required": "Street address 2 field is required"}},
            "I_20_country": {"error_messages": {"required": "Country field is required"}},
            "state": {"error_messages": {"required": "State field is required"}},
            "city": {"error_messages": {"required": "City field is required"}},
        }


class SevisCouponSerializer1(serializers.ModelSerializer):

    class Meta:
        model = SevisInformationUser
        fields = ("user", "form_type", "sevis_coupon")


class SevisCouponSerializer2(serializers.ModelSerializer):
    
    class Meta:
        model = SevisInformationUser
        fields = ("sevis_id", "last_name", "given_name", "date_of_birth", "form", "passport", "international_passport")
        extra_kwargs = {
            "sevis_id": {"error_messages": {"required": "Sevis id field is required"}},
            "last_name": {"error_messages": {"required": "Last name field is required"}},
            "given_name": {"error_messages": {"required": "Given Name field is required"}},
            "date_of_birth": {"error_messages": {"required": "Date of birth field is required"}},
            "form": {"error_messages": {"required": "Form field requires a file to be submitted"}},
            "passport": {"error_messages": {"required": "Passport field requires a file to be submitted"}},
            "international_passport": {"error_messages": {"required": "International Passport field requires a file to be submitted"}},
        }



class SevisCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = SevisInformationUser
        fields = ("user", "form_type", "sevis_coupon", "sevis_id", "last_name", "given_name",
                   "date_of_birth", "form", "passport", "international_passport", "sevis_fee", "fee_in_naira", "fee_in_dollars")
        


class SevisInformationGuestSerializer(serializers.ModelSerializer):

    class Meta:
        model = SevisInformationGuest
        exclude = ["sevis_coupon",]


class SevisCouponGuestSerializer(serializers.ModelSerializer):

    class Meta:
        model = SevisInformationGuest
        fields = ("form_type", "sevis_coupon", "sevis_id", "last_name", "given_name",
                   "date_of_birth", "form", "international_passport", "sevis_fee", 
                   "fee_in_dollars", "fee_in_naira", "charges", "rate", "order_id", "created_at", "payment_status")


class SevisInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SevisInformationUser
        fields = "__all__"