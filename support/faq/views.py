from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from educart_project.permissions import IsStaffOrReadOnly
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class FAQView(APIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = FAQSerializer

    def get(self, request):
        # faqs = Faq.objects.all()
        # serializer = FAQSerializer(faqs, many=True)
        
        payment_queryset = Faq.objects.filter(category="payment")
        payment_serializer = FAQSerializer(payment_queryset, many=True)

        account_queryset = Faq.objects.filter(category="account")
        account_serializer = FAQSerializer(account_queryset, many=True)

        security_queryset = Faq.objects.filter(category="security")
        security_serializer = FAQSerializer(security_queryset, many=True)

        return Response({
            "data": [{
                "title": "Payment",
                "description": "For answers with regards to Sevis Fees, Visa Application, Credential Evaluation, School Application, Payment etc.",
                "image": "https://res.cloudinary.com/dp15stbao/image/upload/v1697539551/EDUCARTS/faq_icons/wsfzsdjrb2brf2hoxivg.png",
                "data": payment_serializer.data,
            }, 

            {
                "title": "Account",
                "description": "For answers with regards to Account Information, Account Details, Creation of Accounts etc.",
                "image": "https://res.cloudinary.com/dp15stbao/image/upload/v1697539551/EDUCARTS/faq_icons/tdglxoi4eel5iyse1i3f.png",
                "data": account_serializer.data,
            },

            {
                "title": "Security",
                "description": "For answers with regards to Pin change, Password change, Card Payments etc.",
                "image": "https://res.cloudinary.com/dp15stbao/image/upload/v1697539551/EDUCARTS/faq_icons/nlsay3ebhvwyptxjxd9v.png",
                "data": security_serializer.data,
            },
            ],
            "message": "Success",
            "error": False,
        }, status=status.HTTP_200_OK)