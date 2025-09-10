from rest_framework import serializers
from .models import Challenge


class ChallengeSerializer(serializers.ModelSerializer):
    """Serializer for Challenge model"""
    
    image_base64 = serializers.SerializerMethodField()
    has_image = serializers.ReadOnlyField()
    
    class Meta:
        model = Challenge
        fields = [
            'id', 'date', 'clue',
            'goals', 'hitareas', 'before_message_body', 'before_message_title',
            'before_message_button', 'before_message_background_image_url',
            'created_at', 'has_image', 'image_base64'
        ]
        read_only_fields = ['id', 'created_at', 'has_image', 'image_base64']
    
    def get_image_base64(self, obj):
        """Return base64 encoded image data"""
        return obj.get_image_base64()


class ChallengeCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Challenge with hitareas as tokenized string and image upload"""
    
    hitareas = serializers.CharField(required=False, allow_blank=True, help_text="Tokenized string of hit areas")
    image = serializers.ImageField(required=False, help_text="Upload an image file")
    
    class Meta:
        model = Challenge
        fields = [
            'date', 'clue', 'image',
            'goals', 'hitareas', 'before_message_body', 'before_message_title',
            'before_message_button', 'before_message_background_image_url'
        ]
    
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