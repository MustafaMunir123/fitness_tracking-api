from django.urls import path, include
from apps.fitness_track import urls as FITNESS_V1_URLS

urlpatterns = [
    path('v1/', include(FITNESS_V1_URLS))
]