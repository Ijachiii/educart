from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),
    path("auth/register/", views.UserSignUpView.as_view(), name="register"),
    path("auth/regenerate-otp/", views.RegenerateOTPView.as_view(), name="regenerate-otp"),
    path("auth/login/", views.LoginView.as_view(), name='token_obtain_pair'),
    path("auth/login/refresh/", views.CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("auth/logout/", views.LogoutView.as_view(), name="logout"),
    path("auth/verify-otp/", views.VerifyOTPView.as_view(), name="user_verify_otp"),
    path("auth/forgot-password/", views.ForgotPasswordView.as_view(), name="forgot_password"),
    path("auth/forgot-password/verify-otp/", views.VerifyOTPView.as_view(), name="verify_otp"),
    path("auth/reset-password/", views.ResetPasswordView.as_view(), name="reset_password"),

    path("account-setup/profile/", views.ProfileView.as_view(), name="profile"),
    path("account-setup/delete/", views.DeleteUserView.as_view(), name="delete_user"),

    path("settings/change-password/", views.ChangePasswordView.as_view(), name="change_password"),
    path("dashboard/order-history/", views.OrderHistoryView.as_view(), name="order_history"),
    path("dashboard/track-order/", views.TrackOrderView.as_view(), name="track_order"),
    path("order-summary/<str:order_type>/", views.OrderSummaryView.as_view(), name="order_summary"),

    
    # path("account-setup/profile/address-book/", views.AddressBookView.as_view(), name="address_book"),
    # path("settings/create-pin./", views.CreatePinView.as_view(), name="create_pin"),
    # path("settings/change-pin/", views.ChangeTransactionPinView.as_view(), name="change_pin"),
    # path("settings/reset-pin-security-questions/", views.SecurityQuestionView.as_view(), name="reset_pin_security_question"),
    # path("settings/reset-pin-otp-verify/", views.VerifyPinChangeOTPView.as_view(), name="reset_pin_otp_verify"),
]