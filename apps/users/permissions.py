from rest_framework import permissions

class IsProUser(permissions.BasePermission):
    """
    Allows access only to PRO users.
    """
    message = "Bu funksiyadan foydalanish uchun PRO obunasi talab qilinadi."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_pro)
