from django.contrib import admin
from .models import Consultation, ConsultationGuest

# Register your models here.
class ConsultationAdmin(admin.ModelAdmin):
    model = Consultation
    list_display = ["user", "consultation", "details", "consultant", "order_id", "fee_in_dollars", "fee_in_naira", "created_at"]

admin.site.register(Consultation, ConsultationAdmin)
admin.site.register(ConsultationGuest)