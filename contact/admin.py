from django.contrib import admin
from .models import ContactMessage
@admin.register(ContactMessage)
class MessageAdmin(admin.ModelAdmin):list_display=['subject','email','created_at','is_read'];list_filter=['is_read'];list_editable=['is_read']
