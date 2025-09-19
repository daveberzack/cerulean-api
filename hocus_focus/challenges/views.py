from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.shortcuts import get_object_or_404
from django.http import Http404

from .models import Challenge
from .serializers import (
    ChallengeSerializer,
    ChallengeCreateSerializer)

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])  # Support file uploads
@permission_classes([AllowAny])  # Public endpoint
def create_challenge(request):
    """
    POST /challenge
    Create a new challenge with optional image upload
    Supports both multipart/form-data (for file uploads) and application/json
    """
    try:
        serializer = ChallengeCreateSerializer(data=request.data)
        if serializer.is_valid():
            challenge = serializer.save()
            # Return the full challenge data with nested objects
            response_serializer = ChallengeSerializer(challenge)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([AllowAny])  # Public endpoint
def get_challenge_by_id(request, challenge_id):
    """
    GET /challenge/{id}
    Get a challenge by ID with all related data
    """
    try:
        challenge = get_object_or_404(Challenge, id=challenge_id)
        serializer = ChallengeSerializer(challenge)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Http404:
        return Response(
            {'error': 'Challenge not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    

# @api_view(['POST'])
# @permission_classes([AllowAny])  # Public endpoint
# def create_christmas_challenge(request):
#     """
#     POST /christmas
#     Create a special Christmas challenge
#     """
#     try:
#         serializer = ChristmasChallengeSerializer(data=request.data)
#         if serializer.is_valid():
#             challenge = serializer.save()
#             # Return the full challenge data with nested objects
#             response_serializer = ChallengeSerializer(challenge)
#             return Response(response_serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     except Exception as e:
#         return Response(
#             {'error': str(e)},
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR
#         )


# @api_view(['GET'])
# @permission_classes([AllowAny])  # Public endpoint
# def get_challenge_image(request, challenge_id):
#     """
#     GET /challenge/{id}/image
#     Get the raw image data for a challenge
#     Returns the actual image file
#     """
#     try:
#         challenge = get_object_or_404(Challenge, id=challenge_id)
        
#         if not challenge.has_image:
#             return Response(
#                 {'error': 'Challenge has no image'},
#                 status=status.HTTP_404_NOT_FOUND
#             )
        
#         # Return the raw image data
#         response = HttpResponse(
#             challenge.image_data,
#             content_type='image/jpeg'  # Default to JPEG
#         )
            
#         return response
        
#     except Http404:
#         return Response(
#             {'error': 'Challenge not found'},
#             status=status.HTTP_404_NOT_FOUND
#         )
#     except Exception as e:
#         return Response(
#             {'error': str(e)},
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR
#         )

