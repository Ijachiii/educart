from django.shortcuts import render
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from accounts.models import OrderHistory
from .models import *
import uuid
from accounts.custom_exception_handler import error_message


def generate_order_id():
    order_id = "CN" + str(uuid.uuid4().hex)[:8].upper()
    try:
        OrderHistory.objects.get(order_id=order_id)
    except OrderHistory.DoesNotExist:
        print(order_id + " success")
        return order_id
    print(order_id + " exists\nRegenerating...")
    generate_order_id()


# Create your views here.
class Consultation1View(APIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = ConsultationSerializer
    CHOICES = [
        {"choice": "Payment for Institution"},
        {"choice": "How to get abroad admission docs"},
        {"choice": "How to apply for admission abroad"},
        {"choice": "Where to get my Visa"},
        {"choice": "Other"}
    ]

    def get(self, request):
        user = request.user
        if not user.profile_completed:
            return Response({
                "data": None,
                "errorMessage": [{
                    "code": "profile_not_completed",
                    "message": "Please complete profile setup"
                }],
                "error": True 
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "data": self.CHOICES,
            "message": "Success",
            "error": False,
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # request.data["user"] = request.user.id
        user = request.user
        serializer = ConsultationSerializer(data=request.data)

        if not user.profile_completed:
            return Response({
                "data": None,
                "errorMessage": [{
                    "code": "profile_not_completed",
                    "message": "Please complete profile setup"
                }],
                "error": True 
            }, status=status.HTTP_400_BAD_REQUEST)

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



class ConsultantListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConsultantListSerializer

    def get(self, request):
        queryset = Consultant.objects.all()
        serializer = ConsultantListSerializer(queryset, many=True)

        return Response({
            "data": serializer.data,
            "message": "Successful",
            "error": None,
        }, status=status.HTTP_200_OK)
    


class ConsultantDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConsultantDetailSerializer

    def get(self, request, pk):
        try:
            queryset = Consultant.objects.get(pk=pk)
            serializer = ConsultantDetailSerializer(queryset)

            return Response({
                "data": serializer.data,
                "message": "Successful",
                "error": None,
            }, status=status.HTTP_200_OK)
        
        except Consultant.DoesNotExist:
            return Response({
                "data":None,
                "errorMessage": [
                    {
                        "code": "invalid_pk",
                        "message": "Consultant does not exist"
                    }
                ],
                "error": True,
            }, status=status.HTTP_404_NOT_FOUND)

    
    def post(self, request, pk):
        user = request.user
        consultation = Consultation.objects.filter(user=user).latest("created_at")
        consultant = Consultant.objects.get(pk=pk)
        charges = 35
        
        if user.free_consultation:
            consultation.consultation_fee = 0
            consultation.fee_in_dollars = 0
            consultation.fee_in_naira = 0
        else:
            consultation.consultation_fee = consultant.price_per_hour
            consultation.fee_in_dollars = consultant.price_per_hour + charges
            consultation.fee_in_naira = consultation.fee_in_dollars * 700

        consultation.consultant = consultant
        order_id = generate_order_id()
        consultation.order_id = order_id

        OrderHistory.objects.create(
            user=user,
            order_id=order_id,
            order_type="Consultation",
            status="Payment Pending",
            amount=consultation.fee_in_naira
        )
        consultation.save()

        user.free_consultation = False
        user.save()

        
        return Response({
            # "data": serializer.data,
            "data": {
                "id": consultation.id,
                "consultation": consultation.consultation,
                "details": consultation.details,
                "fee_in_naira": consultation.fee_in_naira,
                "fee_in_dollars": consultation.fee_in_dollars,
                "order_id": consultation.order_id,
                "created_at": consultation.created_at,
                "user": consultation.user.id,
                "consultant": consultation.consultant.id
            },
            "message": "Success",
            "error": False
        }, status=status.HTTP_200_OK)
            


class ConsultationGuestView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ConsultationGuestSerializer
    CHOICES = [
        {"choice": "Payment for Institution"},
        {"choice": "How to get abroad admission docs"},
        {"choice": "How to apply for admission abroad"},
        {"choice": "Where to get my Visa"},
        {"choice": "Other"}
    ]

    def get(self, request):
        return Response({
            "data": self.CHOICES,
            "message": "Success",
            "error": False,
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ConsultationGuestSerializer(data=request.data)

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
        

# class Consultation2View(APIView):
#     permission_classes = [IsAuthenticated,]
#     serializer_class = ConsultationPage2Serializer

#     def post(self, request):
#         user = request.user
#         instance = Consultation.objects.get(user=user)
#         serializer = ConsultationPage2Serializer(instance, data=request.data)
#         date = request.data.get("date", None)
#         time = request.data.get("time", None)

#         errors = []

#         if serializer.is_valid():
#             consultation_way = request.data.get("consultation_way", None)
#             phone_number = request.data.get("phone_number", None)

#             if consultation_way.lower() == "phone call" and not phone_number:
#                 return Response({
#                     "data": None,
#                     "errorMessage": [{
#                         "code": "empty_phone_field",
#                         "message": "Phone number field is required for phone call"
#                     }],
#                     "error": True
#                 }, status=status.HTTP_400_BAD_REQUEST)
            
#             if not date:
#                 errors.append({
#                     "code": "empty_date_field",
#                     "message": "Date field is required"
#                 })

#             if not time:
#                 errors.append({
#                     "code": "empty_time_field",
#                     "message": "Time field is required"
#                 })
            
#             if errors:
#                 return Response({
#                     "data": None,
#                     "errorMessage": errors,
#                     "error": True
#                 }, status=status.HTTP_400_BAD_REQUEST)
            
#             serializer.save()
#             print(consultation_way)
            
#             return Response({
#                 "data": serializer.data,
#                 "message": "Success",
#                 "error": False
#             }, status=status.HTTP_200_OK)


        
#         for err in serializer.errors:
#             errors.append({
#             "code": f"empty_{err}_field",
#             "message": str(serializer.errors[err][0])
#         })
        
#         if not date:
#             errors.append({
#                 "code": "empty_date_field",
#                 "message": "Date field is required"
#             })

#         if not time:
#             errors.append({
#                 "code": "empty_time_field",
#                 "message": "Time field is required"
#             })
            
#         if errors:
#             return Response({
#                 "data": None,
#                 "errorMessage": errors,
#                 "error": True
#             }, status=status.HTTP_400_BAD_REQUEST)