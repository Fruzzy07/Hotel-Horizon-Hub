

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HotelViewSet, BookingViewSet, CustomerViewSet, ProfileViewSet

router = DefaultRouter()
router.register(r'hotels', HotelViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'profiles', ProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
