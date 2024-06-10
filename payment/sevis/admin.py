from django.contrib import admin
from .models import *

# Register your models here.
class SevisInformationUserAdmin(admin.ModelAdmin):
    model = SevisInformationUser
    list_display = ["user", "sevis_id", "given_name", "last_name", "date_of_birth", "form_type", "category", "fee_in_dollars", "fee_in_naira", "order_id", "payment_status", "created_at"]


class SevisInformationGuestAdmin(admin.ModelAdmin):
    model = SevisInformationGuest
    list_display = ["sevis_id", "given_name", "last_name", "date_of_birth", "form_type", "category", "fee_in_dollars", "fee_in_naira", "order_id", "payment_status", "created_at"]


admin.site.register(SevisInformationUser, SevisInformationUserAdmin)
admin.site.register(SevisInformationGuest, SevisInformationGuestAdmin)