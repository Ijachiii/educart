from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import *

# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "user_type", "first_name", "last_name", "profile_picture", "country_of_residence", 
                    "country_of_birth", "state", "city", "country_code", "phone_number", "institution_of_study", 
                    "wallet_id", "otp", "otp_verified", "otp_expiry", "free_consultation", "profile_completed", "is_restricted", 
                    "is_verified", "is_staff", "is_active",)
    
    list_filter = ("email", "first_name", "last_name", "country_of_residence", 
                    "phone_number", "institution_of_study", "wallet_id", "otp", "otp_expiry", "profile_completed",  
                    "is_verified", "is_staff", "is_active",)
    
    # fieldsets = (
    #     (None, {"fields": ("email", "password", "is_verified", "")}),
    #     ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    # )
    fieldsets = (
        (None, {"fields": ("email", "first_name", "last_name", "password", "profile_picture", "country_of_residence", 
                           "country_code", "phone_number","institution_of_study", "wallet_id", "free_consultation", "profile_completed", 
                           "is_verified")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "user_type", "email", "first_name", "last_name", "password", "profile_picture", "country_of_residence", 
                "is_verified", "country_code", "phone_number", "free_consultation", "institution_of_study", "wallet_id", "otp", "otp_expiry", 
                "password1", "password2", "is_staff", "is_active", "groups", "user_permissions",
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


class OrderHistoryAdmin(admin.ModelAdmin):
    model = OrderHistory
    list_display = ("user", "order_id", "order_type", "amount", "date", "status")


class OrderHistoryGuestAdmin(admin.ModelAdmin):
    model = OrderHistoryGuest
    list_display = ("order_id", "order_type", "amount", "date", "status")


class ConsultantAdmin(admin.ModelAdmin):
    model = Consultant
    list_display = ("user", "name", "profile_picture", "price_per_hour", "specialization", "qualification", "years_of_experience", "state", "country")


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(OrderHistory, OrderHistoryAdmin)
admin.site.register(Consultant, ConsultantAdmin)
admin.site.register(OrderHistoryGuest, OrderHistoryGuestAdmin)
# admin.site.register(AddressBook)
# admin.site.register(SecurityQuestions)
# admin.site.register(SevisInformation)
# admin.site.register(Faq)