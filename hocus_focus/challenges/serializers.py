from rest_framework import serializers
from .models import Challenge


class ChallengeSerializer(serializers.ModelSerializer):
    """Serializer for Challenge model"""
    
    image_base64 = serializers.SerializerMethodField()
    has_image = serializers.ReadOnlyField()
    beforeMessages = serializers.SerializerMethodField()
    
    class Meta:
        model = Challenge
        fields = [
            'id', 'date', 'clue', 'mode', 'theme',
            'goals', 'hitareas', 'beforeMessages',
            'created_at', 'has_image', 'image_base64'
        ]
        read_only_fields = ['id', 'created_at', 'has_image', 'image_base64', 'beforeMessages']
    
    def get_image_base64(self, obj):
        """Return base64 encoded image data"""
        return obj.get_image_base64()
    
    def get_beforeMessages(self, obj):
        """Return before message data as an array with a single element"""
        return [{
            "title": obj.before_message_title or "",
            "body": obj.before_message_body or "",
            "button": obj.before_message_button or "",
            "theme": obj.theme or ""
        }]


class ChallengeCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Challenge with hitareas as tokenized string and image upload"""
    
    hitareas = serializers.CharField(required=False, allow_blank=True, help_text="Tokenized string of hit areas")
    image = serializers.ImageField(required=False, help_text="Upload an image file")
    mode = serializers.CharField(required=False, allow_blank=True, help_text="Challenge mode")
    theme = serializers.CharField(required=False, allow_blank=True, help_text="Theme identifier")
    goals = serializers.CharField(required=False, allow_blank=True, help_text="Comma-separated list of goal times")
    
    class Meta:
        model = Challenge
        fields = [
            'date', 'clue', 'image', 'mode', 'theme',
            'goals', 'hitareas', 'before_message_body', 'before_message_title',
            'before_message_button', 'before_message_background_image_url'
        ]
    
    def create(self, validated_data):
        image_file = validated_data.pop('image', None)
        
        # Handle theme -> background image URL conversion if needed
        theme = validated_data.get('theme')
        if theme and not validated_data.get('before_message_background_image_url'):
            validated_data['before_message_background_image_url'] = f"./img/themes/bgs/{theme}.jpg"
        
        challenge = Challenge.objects.create(**validated_data)
        
        # Handle image upload
        if image_file:
            challenge.set_image_from_file(image_file)
            challenge.save()
        
        return challenge


# class ChristmasChallengeSerializer(serializers.Serializer):
#     """Serializer for Christmas challenge creation"""
    
#     clue = serializers.CharField(required=False, allow_blank=True)
#     before_message = serializers.CharField(required=False, allow_blank=True)
#     before_title = serializers.CharField(required=False, allow_blank=True)
#     theme = serializers.CharField(required=False, default='11')
    
#     def create(self, validated_data):
#         # Create Christmas challenge with default values
#         challenge_data = {
#             'clue': validated_data.get('clue', ''),
#             'goals': [20, 40, 60, 90, 120],
#             'before_message_body': validated_data.get('before_message', ''),
#             'before_message_title': validated_data.get('before_title', ''),
#             'before_message_button': 'Open Card',
#             'before_message_background_image_url': f"./img/themes/bgs/{validated_data.get('theme', '11')}.jpg"
#         }
        
#         challenge = Challenge.objects.create(**challenge_data)
        
#         return challenge