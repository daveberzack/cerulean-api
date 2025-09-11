from django.contrib import admin
from django import forms
from .models import Challenge


class ChallengeAdminForm(forms.ModelForm):
    goals = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text="Enter goals as JSON array, e.g., [30, 60, 90, 120, 150]",
        required=False
    )
    
    class Meta:
        model = Challenge
        fields = '__all__'
        exclude = ['image_data']
    
    def clean_goals(self):
        goals_str = self.cleaned_data.get('goals', '')
        if not goals_str:
            return []
        try:
            import json
            goals = json.loads(goals_str)
            if not isinstance(goals, list):
                raise forms.ValidationError("Goals must be a JSON array")
            return goals
        except json.JSONDecodeError:
            raise forms.ValidationError("Invalid JSON format")


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    form = ChallengeAdminForm
    list_display = ['id', 'clue', 'has_image', 'created_at']
    list_filter = ['created_at']
    search_fields = ['clue']
    readonly_fields = ['created_at', 'has_image']
