from django.urls import path
from . import views

urlpatterns = [
    # Sevis urls for guest
    path("information/guest/", views.SevisInformationGuestView.as_view(), name="sevis-information-guest"),
    path("coupon/guest/", views.SevisCouponGuestView.as_view(), name="sevis-coupon-guest"),

    # Sevis urls for registerd users
    path("information/1/", views.SevisInformationPage1View.as_view(), name="sevis-information-1"),
    path("information/2/", views.SevisInformationPage2View.as_view(), name="sevis-information-2"),
    path("information/3/", views.SevisInformationPage3View.as_view(), name="sevis-information-3"),
    path("coupon/1/", views.SevisCouponView1.as_view(), name="sevis-coupon_1"),
    path("coupon/2/", views.SevisCouponView2.as_view(), name="sevis-coupon_2"),
]