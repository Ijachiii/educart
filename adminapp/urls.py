from django.urls import path
from . import views

urlpatterns = [
    path("faqs/", views.FAQAdminListView.as_view(), name="faq_list"),
    path("faq/<int:pk>/", views.FAQAdminDetailView.as_view(), name="faq"),
    path("consultants/", views.ConsultantAdminListView.as_view(), name="consultant_list"),
    path("consultant/<int:pk>/", views.ConsultantAdminDetailView.as_view(), name="consultant")
]