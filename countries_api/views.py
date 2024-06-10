from django.shortcuts import render
from django.http import  JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination

import json 



# Create your views here.
class CustomPageNumberPagination(PageNumberPagination):
    page_size = 1000  # Set the number of items per page
    page_size_query_param = 'page_size'  # Allow clients to specify page size using a query parameter
    max_page_size = 1000  # Set a maximum page size to prevent abuse


class CountriesView(APIView):
    serializer_class = None

    @method_decorator(cache_page(60*60*2))
    def get(self, request, format=None):
        file_path = "countries_api/countries.json"

        try:
            with open(file_path, 'r') as file:
                data = json.load(file)

            return Response({"data": data,
                                 "message": "Success",
                                 "error": False},
                                 status=status.HTTP_200_OK)
        
        except FileNotFoundError:
            return Response({"data": None,
                                 "errorMessage": [{
                                     "code": "file_not_found",
                                     "message": "File not found"
                                 }], 
                                 "error": True}, status=status.HTTP_404_NOT_FOUND)


        except json.JSONDecodeError:
            return Response({"data": None,
                                  "errorMessage": [{
                                    "code": "invalid_json_file",
                                    "message": "Invalid JSON file"
                                  }], 
                                  "error": True}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class UniversitiesView(APIView):
    serializer_class = None
    pagination_class = CustomPageNumberPagination
    
    @method_decorator(cache_page(60*60*2))
    def get(self, request, format=None):
        file_path = "countries_api/universities.json"

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            
            paginator = self.pagination_class()
            paginated_data = paginator.paginate_queryset(data, request)

            return Response({
                "next": paginator.get_next_link(),
                "previous": paginator.get_previous_link(),
                "data": paginated_data,
                "message": "Success",
                "error": False},
                status=status.HTTP_200_OK)
        
        except FileNotFoundError:
            return Response({"data": None,
                                "errorMessage": [{
                                    "code": "file_not_found",
                                  "  message": "File not found"
                                }], 
                                "error": True}, status=status.HTTP_404_NOT_FOUND)
        

        except json.JSONDecodeError:
            return Response({"data": None,
                                  "errorMessage": [{
                                    "code": "invalid_json_file",
                                    "message": "Invalid JSON file"
                                  }], 
                                  "error": True}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class InstitutionsView(APIView):
    serializer_class = None
    
    @method_decorator(cache_page(60*60*2))
    def get(self, request, format=None):
        file_path = "countries_api/universities.json"

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            return Response({
                "data": data,
                "message": "Success",
                "error": False},
                status=status.HTTP_200_OK)
        
        except FileNotFoundError:
            return Response({"data": None,
                                "errorMessage": [{
                                    "code": "file_not_found",
                                  "  message": "File not found"
                                }], 
                                "error": True}, status=status.HTTP_404_NOT_FOUND)
        

        except json.JSONDecodeError:
            return Response({"data": None,
                                  "errorMessage": [{
                                    "code": "invalid_json_file",
                                    "message": "Invalid JSON file"
                                  }], 
                                  "error": True}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @csrf_exempt
# def jsonview(request):

#     if request.method == "GET":
#         with open("countries_api/final_json.json", "r") as file:
#             data = json.load(file)

#         return JsonResponse({"data": data, "message": "Success", "error": False}, safe=False, status=200)

# class CountriesView(APIView):
#     def get(self, request, format=None):
#         file_path = "countries_api/cleaned.json"

#         try:
#             with open(file_path, 'r') as file:
#                 data = json.load(file)
#             return JsonResponse({"data": data,
#                                  "message": "Success",
#                                  "error": False}, 
#                                  safe=False, 
#                                  status=200)
#         except FileNotFoundError:
#             return JsonResponse({"data": None,
#                                   "errorMessage": [{
#                                     "code": "file_not_found",
#                                     "message": "File not found"
#                                   }], 
#                                   "error": True}, status=404)
#         except json.JSONDecodeError:
#             return JsonResponse({"data": None,
#                                   "errorMessage": [{
#                                     "code": "invalid_json_file",
#                                     "message": "Invalid JSON file"
#                                   }], 
#                                   "error": True}, status=500)
        

