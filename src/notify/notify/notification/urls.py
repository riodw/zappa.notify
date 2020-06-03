# Django
from django.conf.urls import include
from django.urls import path
# Rest
from rest_framework import routers
# App
from .viewsets import (
    NotificationViewSet,
    EmailViewSet,
    SMSViewSet,
    PushViewSet,
    RunViewSet,
)

# Routers
router = routers.DefaultRouter()

# 
router.register(
    r'notification',
    NotificationViewSet,
    'notification',
)
router.register(
    r'email',
    EmailViewSet,
    'email',
)
router.register(
    r'sms',
    SMSViewSet,
    'sms',
)
router.register(
    r'push',
    PushViewSet,
    'push',
)
router.register(
    r'run',
    RunViewSet,
    'run',
)


# Include Routers
urlpatterns = [
    path('', include(router.urls)),
]