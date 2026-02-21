
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import PropertyModelViewSet, UserModelViewSet, LeaseModelViewSet, RegisterApiView, AnnouncementModelViewSet, MetersModelViewSet, BillModelViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('register', RegisterApiView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]

router = DefaultRouter()
router.register(r'properties', PropertyModelViewSet, basename='property')
router.register(r'users', UserModelViewSet, basename='user')
router.register(r'leases', LeaseModelViewSet, basename='lease')
router.register(r'announcements', AnnouncementModelViewSet,
                basename='announcement')
router.register(r'meters', MetersModelViewSet,
                basename='meters')
router.register(r'bills', BillModelViewSet,
                basename='bill')


urlpatterns += router.urls
