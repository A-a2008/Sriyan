from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get_audio_files/', views.get_updated_audio_files, name='get_audio_files'),
]