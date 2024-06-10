from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import NewsletterSerializer
from rest_framework.permissions import AllowAny
from .models import Newsletter
from rest_framework import status
from educart_project.permissions import IsStaffOrPostOnly
from accounts.custom_exception_handler import error_message


# Create your views here.
class NewsletterView(APIView):
    permission_classes = [AllowAny, IsStaffOrPostOnly]
    serializer_class = NewsletterSerializer

    def get(self, request):
        queryset = Newsletter.objects.all()
        serializer = NewsletterSerializer(queryset, many=True)

        return Response({
            "data": serializer.data,
            "message": "Success",
            "error": False
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = NewsletterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            
            return Response({
                "data": serializer.data,
                "message": "Success",
                "error": False
            }, status=status.HTTP_200_OK)
        
        return Response({
            "data": None,
            "errorMessage": error_message(serializer),
            "error": True
        }, status=status.HTTP_400_BAD_REQUEST)