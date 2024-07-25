from rest_framework import routers
from map.api.views import LoginViewSet, DatabolgeViewSet, DatayolViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'databolge',DatabolgeViewSet,basename='databolge')
router.register(r'datayol',DatayolViewSet,basename='datayol')
router.register(r'login', LoginViewSet, basename='login')
urlpatterns = [
    path('', include(router.urls)),
    path('auth', include('rest_framework.urls', namespace='rest_framework')),
]