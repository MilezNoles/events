from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):

        if request.user.is_staff:
            return True

        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user


class IsEventMaker(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated
                    and (request.method in SAFE_METHODS
                         or request.user.is_event_creator))

    def has_object_permission(self, request, view, obj):

        if request.user.is_staff:
            return True

        if request.user.is_event_creator:
            return True

        if request.method in SAFE_METHODS:
            return True

        return False
