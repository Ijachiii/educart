from django.urls import path
from . import views

urlpatterns = [
    path("countries/", views.CountriesView.as_view(), name="countries"),
    path("universities/", views.UniversitiesView.as_view(), name="universities"),
    path("institutions/", views.InstitutionsView.as_view(), name="uni"),
]