from django.urls import path
from .views import register_company, check_domain

urlpatterns = [
    path('', register_company, name='register'),
    path('check-domain/', check_domain, name='check_domain'),
]
