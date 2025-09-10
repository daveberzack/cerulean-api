from django.contrib import admin
from django.utils.html import format_html
from .models import Challenge


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ['id', 'clue', 'has_image', 'image_name', 'image_size_kb', 'created_at']
    list_filter = ['is_test', 'is_permanent', 'is_tutorial', 'created_at']
    search_fields = ['clue', 'credit', 'image_name']
    readonly_fields = ['created_at', 'updated_at', 'has_image', 'image_size_kb', 'image_preview']
    
    def image_size_kb(self, obj):
        """Display image size in KB"""
        if obj.image_size:
            return f"{obj.image_size // 1024} KB"
        return "No image"
    image_size_kb.short_description = "Image Size"
    
    def image_preview(self, obj):
        """Display image preview in admin"""
        if obj.has_image:
            return format_html(
                '<img src="data:{};base64,{}" style="max-width: 200px; max-height: 200px;" />',
                obj.image_content_type,
                obj.get_image_base64()
            )
        return "No image"
    image_preview.short_description = "Image Preview"
