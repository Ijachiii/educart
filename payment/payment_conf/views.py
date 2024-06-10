from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from accounts.models import *
from django.contrib.auth.models import AnonymousUser
from accounts.custom_exception_handler import error_message

# Create your views here.
class ReceiptUploadView(APIView):
    permission_classes = [AllowAny,]
    serializer_class = ReceiptUploadSerializer

    def post(self, request):
        user = request.user
        serializer = ReceiptUploadSerializer(data=request.data)
        
        if serializer.is_valid():
            order_id = request.data.get("order_id")

            order = OrderHistoryGuest.objects.filter(order_id=order_id).order_by("date")
            order_model = "guest"
            if len(order) < 1:
                order = OrderHistory.objects.filter(order_id=order_id).order_by("date")
                order_model = "user"
                if len(order) < 1:
                    return Response({
                        "data": None,
                        "errorMessage": [{
                            "code": "invalid_order_id",
                            "message": "Order ID does not exist"
                        }],
                        "error": True 
                    }, status=status.HTTP_400_BAD_REQUEST)
                
            print(order_model)
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": "Success",
                "error": False
            })
            

        return Response({
            "data": None,
            "errorMessage": error_message(serializer),
            "error": True
        }, status=status.HTTP_400_BAD_REQUEST)