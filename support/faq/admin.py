from django.contrib import admin
from .models import Faq

# Register your models here.
class FaqAdmin(admin.ModelAdmin):
    model = Faq
    list_display = ("question", "answer", "category")

admin.site.register(Faq, FaqAdmin)