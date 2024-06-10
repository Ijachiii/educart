from django.contrib import admin
from .models import Newsletter

# Register your models here.
class NewsletterAdmin(admin.ModelAdmin):
    model = Newsletter
    list_display = ["email", "created_at"]


admin.site.register(Newsletter, NewsletterAdmin)