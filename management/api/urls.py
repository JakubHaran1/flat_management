
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import PropertyModelViewSet, UserModelViewSet
urlpatterns = [


]

router = DefaultRouter()
router.register(r'properties', PropertyModelViewSet, basename='property')
router.register(r'users', UserModelViewSet, basename='user')
router.register(r'leases', UserModelViewSet, basename='lease')


urlpatterns += router.urls
