from django.contrib import admin
from .models import BlogPost,Category
@admin.register(BlogPost)
class BlogAdmin(admin.ModelAdmin):
 list_display=['title','author','category','status','created_at']
 list_filter=['status','category']
 search_fields=['title','author__username']
 actions=['approve_posts']
 @admin.action(description='Approve selected posts')
 def approve_posts(self,request,queryset):queryset.update(status='published')
admin.site.register(Category)
