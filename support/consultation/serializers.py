from rest_framework import serializers
from .models import Consultation, ConsultationGuest
from accounts.models import Consultant


class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = "__all__"
        extra_kwargs = {
            "consultation": {"error_messages": {"required": "Consultation field is required"}},
            "details": {"error_messages": {"required": "Detail field is required"}},
        }


class ConsultationGuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultationGuest
        fields = "__all__"


class ConsultantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultant
        exclude = ("bio", "qualification")


class ConsultantDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultant
        fields = "__all__"


# class ConsultationPage2Serializer(serializers.ModelSerializer):
#     class Meta:
#         model = Consultation
#         fields = ("consultation_way", "phone_number", "time_of_consultation", "date", "time")
#         extra_kwargs = {
#             "consultation_way": {"error_messages": {"required": "Way of consultation field is required"}},
#             "time_of_consultation": {"error_messages": {"required": "Time of Consultation field is required"}},
#             "date": {"error_messages": {"required": "Date field is required"}},
#             "time": {"error_messages": {"required": "Time field is required"}}
#         }