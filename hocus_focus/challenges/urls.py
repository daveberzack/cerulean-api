from django.urls import path
from . import views

urlpatterns = [
    path('challenge', views.create_challenge, name='create_challenge'),
    path('challenge/<int:challenge_id>', views.get_challenge_by_id, name='get_challenge_by_id'),
]