from rest_framework import serializers
from .models import Faq

class FAQSerializer(serializers.ModelSerializer):

    class Meta:
        model = Faq
        fields = "__all__"
        extra_kwargs = {
            "question": {"error_messages": {"required": "Question field is required"}},
            "answer": {"error_messages": {"required": "Answer field is required"}}
        }