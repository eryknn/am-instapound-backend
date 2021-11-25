from rest_framework import permissions


class IsPictureCreatorOrSafeOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or view.action == 'like':
            return True

        return obj.uploaded_by == request.user


class IsPictureCommentCreatorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.created_by == request.user
