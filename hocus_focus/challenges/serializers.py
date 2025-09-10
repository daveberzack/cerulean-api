from rest_framework import serializers
from .models import Challenge
import base64


class ChallengeSerializer(serializers.ModelSerializer):
    """Serializer for Challenge model"""
    
    image_base64 = serializers.SerializerMethodField()
    has_image = serializers.ReadOnlyField()
    
    class Meta:
        model = Challenge
        fields = [
            'id', 'date', 'clue', 'credit', 'credit_url',
            'goals', 'hitareas', 'before_message_body', 'before_message_title',
            'before_message_button', 'before_message_background_image_url',
            'is_test', 'is_permanent', 'is_tutorial', 'created_at', 'updated_at',
            'image_name', 'image_content_type', 'image_size', 'has_image', 'image_base64'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'has_image', 'image_base64']
    
    def get_image_base64(self, obj):
        """Return base64 encoded image data"""
        return obj.get_image_base64()


class ChallengeCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Challenge with hitareas as tokenized string and image upload"""
    
    hitareas = serializers.CharField(required=False, allow_blank=True, help_text="Tokenized string of hit areas")
    image = serializers.ImageField(required=False, help_text="Upload an image file (max 100KB)")
    
    class Meta:
        model = Challenge
        fields = [
            'date', 'clue', 'credit', 'credit_url', 'image',
            'goals', 'hitareas', 'before_message_body', 'before_message_title',
            'before_message_button', 'before_message_background_image_url',
            'is_test', 'is_permanent', 'is_tutorial'
        ]
    
    def validate_image(self, value):
        """Validate image file size (max 100KB)"""
        if value:
            max_size = 100 * 1024  # 100KB in bytes
            if value.size > max_size:
                raise serializers.ValidationError(
                    f"Image file too large. Maximum size is {max_size // 1024}KB. "
                    f"Current size is {value.size // 1024}KB."
                )
            
            # Validate file type
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
            if value.content_type not in allowed_types:
                raise serializers.ValidationError(
                    f"Unsupported image type: {value.content_type}. "
                    f"Allowed types: {', '.join(allowed_types)}"
                )
        
        return value
    
    def create(self, validated_data):
        image_file = validated_data.pop('image', None)
        
        challenge = Challenge.objects.create(**validated_data)
        
        # Handle image upload
        if image_file:
            challenge.set_image_from_file(image_file)
            challenge.save()
        
        return challenge


class ChristmasChallengeSerializer(serializers.Serializer):
    """Serializer for Christmas challenge creation"""
    
    clue = serializers.CharField(required=False, allow_blank=True)
    before_message = serializers.CharField(required=False, allow_blank=True)
    before_title = serializers.CharField(required=False, allow_blank=True)
    theme = serializers.CharField(required=False, default='11')
    
    def create(self, validated_data):
        # Create Christmas challenge with default values
        challenge_data = {
            'clue': validated_data.get('clue', ''),
            'goals': [20, 40, 60, 90, 120],
            'before_message_body': validated_data.get('before_message', ''),
            'before_message_title': validated_data.get('before_title', ''),
            'before_message_button': 'Open Card',
            'before_message_background_image_url': f"./img/themes/bgs/{validated_data.get('theme', '11')}.jpg"
        }
        
        challenge = Challenge.objects.create(**challenge_data)
        
        return challenge