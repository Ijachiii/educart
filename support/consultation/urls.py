from django.urls import path
from . import views


urlpatterns = [
    path("consultation/1/", views.Consultation1View.as_view(), name="consultation"),
    # path("consultation/1/", views.ConsultationView.as_view(), name="consultation"),
    path("consultants/", views.ConsultantListView.as_view(), name="consultant-list"),
    path("consultants/<int:pk>/", views.ConsultantDetailView.as_view(), name="consultant-detail"),
    # path("consultation/guest/", views.ConsultationGuestView.as_view(), name="consultation-guest"),
]