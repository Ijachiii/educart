from rest_framework import serializers
from support.faq.models import Faq
from accounts.models import Consultant

class FAQAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = Faq
        fields = "__all__"
        extra_kwargs = {
            "question": {"error_messages": {"required": "Question field is required"}},
            "answer": {"error_messages": {"required": "Answer field is required"}}
        }


class ConsultantAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = Consultant
        fields = "__all__"
