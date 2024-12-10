from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'hotels', views.HotelViewSet)
router.register(r'rooms', views.RoomViewSet)
router.register(r'customers', views.CustomerViewSet)
router.register(r'bookings', views.BookingViewSet)
router.register(r'pricing', views.PricingViewSet)
router.register(r'reports', views.ReportViewSet)

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),

    # Hotel views
    path('hotels/', views.hotel_list, name='hotel_list'),
    path('hotels/create/', views.hotel_create, name='hotel_create'),  # Add this line
    path('hotels/<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),

    # Room views
    path('hotels/<int:hotel_id>/rooms/', views.room_list, name='room_list'),
    path('hotels/<int:hotel_id>/rooms/create/', views.room_create, name='room_create'),
    path('rooms/<int:room_id>/', views.room_detail, name='room_detail'),

    # Customer views
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/create/', views.customer_create, name='customer_create'),
    path('customers/<int:customer_id>/', views.customer_detail, name='customer_detail'),

    # Booking views
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/create/<int:hotel_id>/', views.booking_create, name='booking_create'),
    path('bookings/<int:booking_id>/', views.booking_detail, name='booking_detail'),

    # Pricing views
    path('pricing/', views.pricing_list, name='pricing_list'),
    path('pricing/create/', views.pricing_create, name='pricing_create'),
    path('pricing/<int:pricing_id>/', views.pricing_detail, name='pricing_detail'),

    # Report views
    path('hotels/<int:hotel_id>/reports/', views.report_list, name='report_list'),
    path('hotels/<int:hotel_id>/reports/create/', views.report_create, name='report_create'),
    path('reports/<int:report_id>/', views.report_detail, name='report_detail'),
]


