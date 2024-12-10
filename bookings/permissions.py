from rest_framework import permissions

from .models import Room, Report


class IsCustomerUser(permissions.BasePermission):
    """
    Разрешение, которое позволяет только пользователю с ролью CustomerUser
    видеть только свободные номера и создавать отчеты.
    """

    def has_permission(self, request, view):
        # Проверка, является ли пользователь обычным клиентом
        return request.user and request.user.is_authenticated and request.user.role == 'customer'

    def has_object_permission(self, request, view, obj):
        # Разрешение только на чтение свободных номеров и создание отчетов
        if isinstance(obj, Room):
            # Допустим, свободные номера - те, у которых нет бронирования
            return obj.is_available
        if isinstance(obj, Report):
            # Разрешение на создание отчетов для всех пользователей с ролью 'customer'
            return True
        return False


class IsManagerOrAdmin(permissions.BasePermission):
    """
    Разрешение для администраторов и менеджеров, которые имеют доступ ко всем данным.
    """

    def has_permission(self, request, view):
        # Проверка, является ли пользователь менеджером или администратором
        return request.user and request.user.is_authenticated and (
                request.user.role == 'admin' or request.user.role == 'manager'
        )

    def has_object_permission(self, request, view, obj):
        # Менеджеры и администраторы могут видеть/редактировать все объекты
        return True

