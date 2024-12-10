from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Hotel, Customer, Booking, Pricing, Room

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'is_staff', 'is_active', 'date_joined']  # Include role
    list_filter = ['role', 'is_staff', 'is_active']  # Filter by role, if needed
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),  # Add role field to the form
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),  # Add role when creating new user
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Hotel)
admin.site.register(Customer)
admin.site.register(Booking)
admin.site.register(Room)
admin.site.register(Pricing)


