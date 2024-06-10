from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import re
import uuid
from accounts.models import OrderHistory, OrderHistoryGuest
from .models import *
from .utils import send_congratulatory_sevis
from accounts.custom_exception_handler import error_message


def generate_order_id():
    order_id = "SE" + str(uuid.uuid4().hex)[:8].upper()
    try:
        SevisInformationUser.objects.get(order_id=order_id)

    except SevisInformationUser.DoesNotExist:
        try:
            SevisInformationGuest.objects.get(order_id=order_id)
        
        except SevisInformationGuest.DoesNotExist:
            print(order_id)
            return order_id
        print(order_id)
        generate_order_id()

    print(order_id)
    generate_order_id()


# Create your views here.
class SevisInformationPage1View(APIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = SevisInformationPage1Serializer

    def post(self, request, format=None):
        # request.data["user"] = request.user.id
        serializer = SevisInformationPage1Serializer(data=request.data)
        print(serializer.initial_data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": "Successful",
                "error": False
            }, status=status.HTTP_200_OK)

        return Response({
            "data": None,
            "errorMessage": error_message(serializer),
            "error": True
        }, status=status.HTTP_400_BAD_REQUEST)



class SevisInformationPage2View(APIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = SevisInformationPage2Serializer
    CHOICES = [
        {"choice": "au pair ($35)"},
        {"choice": "camp counselor ($35)"},
        {"choice": "summer work/travel ($35)"},
        {"choice": "others ($200)"},
    ]

    def get(self, request):
        return Response({
            "data": self.CHOICES,
            "message": "Success",
            "error": False
        }, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        # instance = SevisInformationUser.objects.get(user=user)
        instance = SevisInformationUser.objects.filter(user=user).latest("created_at")
        serializer = SevisInformationPage2Serializer(instance, data=request.data)
        print(serializer.initial_data)

        if serializer.is_valid():
            fee = 0
            if "category" in request.data:
                try:
                    fee = int(re.sub("[$)]", "", request.data["category"].split("(")[1]))
                except IndexError:
                    fee = 0

            charges = 35
            
            sevis_fee = 350 + fee
            total_fee_dollars = sevis_fee + charges
            print(f"${total_fee_dollars}")

            total_fee_naira = total_fee_dollars * 700
            print(f"N{total_fee_naira}")

            serializer.save(sevis_fee=sevis_fee, fee_in_naira=total_fee_naira, fee_in_dollars=total_fee_dollars)

            return Response({
                "data": serializer.data,
                "message": "Successful",
                "error": False
            }, status=status.HTTP_200_OK)


        errors = []
        
        return Response({
            "data": None,
            "errorMessage": error_message(serializer),
            "error": True
        }, status=status.HTTP_400_BAD_REQUEST)


class SevisInformationPage3View(APIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = SevisInformationPage3Serializer

    def post(self, request):
        user = request.user
        # instance = SevisInformationUser.objects.get(user=user)
        instance = SevisInformationUser.objects.filter(user=user).latest("created_at")
        serializer = SevisInformationPage3Serializer(instance, data=request.data)
        print(serializer.initial_data)

        if serializer.is_valid():
            serializer.save()
            # sevis = SevisInformationUser.objects.get(user=user)
            sevis = SevisInformationUser.objects.filter(user=user).latest("created_at")
            order_id = generate_order_id()
            order = OrderHistory.objects.create(user=user, 
                                                order_id=order_id, 
                                                order_type="SEVIS Fee/"+sevis.form_type, 
                                                status="Payment Pending", 
                                                amount=sevis.fee_in_naira)
            sevis.order_id = order_id
            send_congratulatory_sevis(email=sevis.email,
                                      name=sevis.given_name,
                                      order_id=order_id,
                                      amount=sevis.fee_in_naira, 
                                      form_type="SEVIS Fee/"+sevis.form_type)
            sevis.save()
            order.save()
            ser = SevisInformationSerializer(sevis)

            return Response({
                "data": ser.data,
                "message": "Successful",
                "error": False
            }, status=status.HTTP_200_OK)
        
        return Response({
            "data": None,
            "errorMessage": error_message(serializer),
            "error": True
        }, status=status.HTTP_400_BAD_REQUEST)
    


class SevisCouponView1(APIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = SevisCouponSerializer1
    
    def post(self, request):
        serializer = SevisCouponSerializer1(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({
                "data": serializer.data,
                "message": "Success",
                "error": False,
            }, status=status.HTTP_200_OK)
        
        return Response({
            "data": None,
            "errorMessage": error_message(serializer),
            "error": True
        }, status=status.HTTP_400_BAD_REQUEST)


class SevisCouponView2(APIView):
    permission_classes = [IsAuthenticated,]
    serializer_class =SevisCouponSerializer2
    
    def post(self, request):
        user = request.user
        # instance = SevisInformationUser.objects.get(user=user)
        instance = SevisInformationUser.objects.filter(user=user).latest("created_at")
        serializer = SevisCouponSerializer2(instance, data=request.data)

        if serializer.is_valid():
            charges = 35
            sevis_fee = 350
            total_fee_dollars = sevis_fee + charges

            total_fee_naira = total_fee_dollars * 700

            serializer.save(sevis_fee=sevis_fee, fee_in_naira=total_fee_naira, fee_in_dollars=total_fee_dollars)

            # sevis = SevisInformationUser.objects.get(user=user)
            sevis = SevisInformationUser.objects.filter(user=user).latest("created_at")

            order_id = generate_order_id()
            order = OrderHistory.objects.create(user=user, 
                                                order_id=order_id, 
                                                order_type="SEVIS Fee/"+sevis.form_type, 
                                                status="Payment Pending", 
                                                amount=sevis.fee_in_naira)
            sevis.order_id = order_id
            sevis.save()
            order.save()

            ser = SevisCouponSerializer(sevis)

            return Response({
                "data": ser.data,
                "message": "Success",
                "error": False,
            }, status=status.HTTP_200_OK)
        
        return Response({
            "data": None,
            "errorMessage": error_message(serializer),
            "error": True
        }, status=status.HTTP_400_BAD_REQUEST)
    


class SevisInformationGuestView(APIView):
    permission_classes = [AllowAny,]
    serializer_class = SevisInformationGuestSerializer

    CHOICES = [
        {"category": "au pair ($35)"},
        {"category": "camp counselor ($35)"},
        {"category": "summer work/travel ($35)"},
        {"category": "others ($200)"},
    ]

    def get(self, request):
        return Response({
            "data": self.CHOICES,
            "message": "Success",
            "error": False
        }, status=status.HTTP_200_OK)
    

    def post(self, request, format=None):
        serializer = SevisInformationGuestSerializer(data=request.data)
        print(serializer.initial_data)
        
        if serializer.is_valid():
            fee = 0
            if "category" in request.data:
                try:
                    fee = int(re.sub("[$)]", "", request.data["category"].split("(")[1]))
                except IndexError:
                    fee = 0

            print(fee)
            charges = 35
            
            sevis_fee = 350 + fee
            total_fee_dollars = sevis_fee + charges
            print(f"${total_fee_dollars}")

            total_fee_naira = total_fee_dollars * 700
            print(f"N{total_fee_naira}")

            order_id = generate_order_id()
            payment_status = "Payment Pending"
            serializer.save(sevis_fee=sevis_fee, order_id=order_id, fee_in_naira=total_fee_naira, 
                            fee_in_dollars=total_fee_dollars, payment_status=payment_status)

            order = OrderHistoryGuest.objects.create(order_id=order_id, 
                                                order_type="SEVIS Fee/"+serializer.data["form_type"], 
                                                status="Payment Pending", 
                                                amount=serializer.data["fee_in_naira"])
            
            
            send_congratulatory_sevis(email=serializer.data["email"],
                                      name=serializer.data["given_name"],
                                      order_id=order_id,
                                      amount=total_fee_naira, 
                                      form_type="SEVIS Fee/"+serializer.data["form_type"])

            order.save()

            return Response({
                "data": serializer.data,
                "message": "Action successful!",
                "error": False,
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "data": None,
            "errorMessage": error_message(serializer),
            "error": True
        }, status=status.HTTP_400_BAD_REQUEST)



class SevisCouponGuestView(APIView):
    permission_classes = [AllowAny,]
    serializer_class = SevisCouponGuestSerializer

    def post(self, request):
        serializer = SevisCouponGuestSerializer(data=request.data)
        
        if serializer.is_valid():
            charges = 35
            sevis_fee = 350
            total_fee_dollars = sevis_fee + charges

            total_fee_naira = total_fee_dollars * 700
            payment_status = "Payment Pending"
            order_id = generate_order_id()

            serializer.save(sevis_fee=sevis_fee, order_id=order_id, fee_in_naira=total_fee_naira, 
                            fee_in_dollars=total_fee_dollars, payment_status=payment_status)

            return Response({
                "data": serializer.data,
                "message": "Success",
                "error": False,
            }, status=status.HTTP_200_OK)
        
        return Response({
            "data": None,
            "errorMessage": error_message(serializer),
            "error": True
        }, status=status.HTTP_400_BAD_REQUEST)