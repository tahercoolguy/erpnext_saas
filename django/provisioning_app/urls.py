from django.urls import path
from .views import register_company

urlpatterns = [
    path('', register_company, name='register'),
]
