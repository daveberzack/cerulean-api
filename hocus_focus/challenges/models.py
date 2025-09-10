from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
import uuid
import base64


class Challenge(models.Model):
    """Challenge model representing a Hocus Focus puzzle"""
    
    id = models.AutoField(primary_key=True)
    date = models.CharField(max_length=50, blank=True, null=True)
    clue = models.TextField()
    credit = models.CharField(max_length=255, blank=True, null=True)
    credit_url = models.URLField(blank=True, null=True)
    # Image storage fields
    image_data = models.BinaryField(blank=True, null=True, help_text="Binary image data")
    image_name = models.CharField(max_length=255, blank=True, null=True, help_text="Original filename")
    image_content_type = models.CharField(max_length=100, blank=True, null=True, help_text="MIME type (e.g., image/jpeg)")
    image_size = models.PositiveIntegerField(blank=True, null=True, help_text="File size in bytes")
    goals = models.JSONField(default=list)  # List of integers for time goals
    hitareas = models.TextField(blank=True, null=True, help_text="Tokenized string of hit areas")
    
    # Before message fields (1-to-1 relationship, so included directly)
    before_message_body = models.TextField(blank=True, null=True)
    before_message_title = models.CharField(max_length=255, blank=True, null=True)
    before_message_button = models.CharField(max_length=100, blank=True, null=True)
    before_message_background_image_url = models.URLField(blank=True, null=True)
    
    is_test = models.BooleanField(default=False, null=True, blank=True)
    is_permanent = models.BooleanField(default=False, null=True, blank=True)
    is_tutorial = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'challenges'
        ordering = ['-created_at']

    def __str__(self):
        return f"Challenge {self.id}: {self.clue[:50]}"
    
    @property
    def has_image(self):
        """Check if challenge has an image"""
        return self.image_data is not None
    
    def get_image_base64(self):
        """Get image as base64 encoded string for API responses"""
        if self.image_data:
            return base64.b64encode(self.image_data).decode('utf-8')
        return None
    
    def set_image_from_file(self, uploaded_file):
        """Set image data from uploaded file"""
        if uploaded_file:
            self.image_data = uploaded_file.read()
            self.image_name = uploaded_file.name
            self.image_content_type = uploaded_file.content_type
            self.image_size = uploaded_file.size
            # Reset file pointer for potential reuse
            uploaded_file.seek(0)


