from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from educart_project.permissions import IsStaffOrReadOnly
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status

from support.faq.models import Faq
from accounts.models import Consultant
from accounts.custom_exception_handler import error_message

# Create your views here.

class FAQAdminListView(APIView):
    permission_classes = [IsAdminUser,]
    serializer_class = FAQAdminSerializer

    def get(self, request, format=None):
        faqs = Faq.objects.all()    
        serializer = FAQAdminSerializer(faqs, many=True)

        return Response({
            "data": serializer.data,
            "message": "Success",
            "error": False
        }, status=status.HTTP_200_OK)
        
    
    def post(self, request):
        serializer = FAQAdminSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": "Successfully created FAQ",
                "error": False
            }, status=status.HTTP_200_OK)

        return Response({
            "data": None,
            "errorMessage": error_message(serializer),
            "error": True
        }, status=status.HTTP_400_BAD_REQUEST)
    

class FAQAdminDetailView(APIView):
    permission_classes = [IsAdminUser,]
    serializer_class = FAQAdminSerializer

    def get(self, request, pk=None, format=None):
        try:
            faq = Faq.objects.get(pk=pk)
        except Faq.DoesNotExist:
            return Response({
                "data": None,
                "errorMessage": [{
                    "code": "invalid_pk",
                    "message": "FAQ with this pk does not exist"
                }],
                "error": True
            }, status=status.HTTP_400_BAD_REQUEST)
            
        serializer = FAQAdminSerializer(faq)
        return Response({
            "data": serializer.data,
            "message": "Success",
            "error": False
        }, status=status.HTTP_200_OK)


    def patch(self, request, pk=None, format=None):
        try:
            faq = Faq.objects.get(pk=pk)
        except Faq.DoesNotExist:
            return Response({
                "data": None,
                "errorMessage": [{
                    "code": "invalid_pk",
                    "message": "FAQ with this pk does not exist"
                }],
                "error": True
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = FAQAdminSerializer(faq, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": "FAQ updated successfully",
                "error": False
            }, status=status.HTTP_200_OK)
        

        return Response({
            "data": None,
            "errorMessage": error_message(serializer),
            "error": True
        }, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk=None, format=None):
        try:
            faq = Faq.objects.get(pk=pk)
        except Faq.DoesNotExist:
            return Response({
                "data": None,
                "errorMessage": [{
                    "code": "invalid_pk",
                    "message": "FAQ with this pk does not exist"
                }],
                "error": True
            }, status=status.HTTP_400_BAD_REQUEST)
        
        faq.delete()

        return Response({
            "data": None,
            "message": "FAQ deleted successfully",
            "error": False
        }, status=status.HTTP_200_OK)
    


class ConsultantAdminListView(APIView):
    permission_classes = [IsAdminUser,]
    serializer_class = ConsultantAdminSerializer

    def get(self, request, format=None):
        consultants = Consultant.objects.all()
        serializer = ConsultantAdminSerializer(consultants, many=True)

        return Response({
            "data": serializer.data,
            "message": "Success",
            "error": False
        }, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = ConsultantAdminSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": "Successfully created consultant!",
                "error": False
            }, status=status.HTTP_200_OK)
        

        return Response({
            "data": None,
            "errorMessage": error_message(serializer),
            "error": True
        }, status=status.HTTP_400_BAD_REQUEST)



class ConsultantAdminDetailView(APIView):
    permission_classes = [IsAdminUser,]
    serializer_class = ConsultantAdminSerializer

    def get(self, request, pk=None, format=None):
        try:
            consultant = Consultant.objects.get(pk=pk)
        except Consultant.DoesNotExist:
            return Response({
                "data": None,
                "errorMessage": [{
                    "code": "invalid_pk",
                    "message": "Consultant with this pk does not exist"
                }],
                "error": True
            }, status=status.HTTP_400_BAD_REQUEST)
            
        serializer = ConsultantAdminSerializer(consultant)
        return Response({
            "data": serializer.data,
            "message": "Success",
            "error": False
        }, status=status.HTTP_200_OK)


    def patch(self, request, pk=None, format=None):
        try:
            consultant = Consultant.objects.get(pk=pk)
        except Consultant.DoesNotExist:
            return Response({
                "data": None,
                "errorMessage": [{
                    "code": "invalid_pk",
                    "message": "Consultant with this pk does not exist"
                }],
                "error": True
            }, status=status.HTTP_400_BAD_REQUEST)
            
        serializer = ConsultantAdminSerializer(consultant, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": "Consultant updated successfully",
                "error": False
            }, status=status.HTTP_200_OK)
        
        return Response({
            "data": None,
            "errorMessage": error_message(serializer),
            "error": True
        }, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk=None, format=None):
        try:
            consultant = Consultant.objects.get(pk=pk)
        except Consultant.DoesNotExist:
            return Response({
                "data": None,
                "errorMessage": [{
                    "code": "invalid_pk",
                    "message": "Consultant with this pk does not exist"
                }],
                "error": True
            }, status=status.HTTP_400_BAD_REQUEST)
        
        consultant.delete()

        return Response({
            "data": None,
            "message": "Consultant Deleted Successfully",
            "error": False
        }, status=status.HTTP_200_OK)