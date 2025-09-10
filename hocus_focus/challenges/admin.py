from django.contrib import admin
from .models import Challenge


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ['id', 'clue', 'has_image', 'created_at']
    list_filter = ['created_at']
    search_fields = ['clue']
    readonly_fields = ['created_at', 'has_image']
