from django.urls import path
from . import views

urlpatterns = [
    path('challenge', views.create_challenge, name='create_challenge'),
    path('christmas', views.create_christmas_challenge, name='create_christmas_challenge'),
    path('challenge/<int:challenge_id>', views.get_challenge_by_id, name='get_challenge_by_id'),
    path('challenge/<int:challenge_id>/image', views.get_challenge_image, name='get_challenge_image'),
]