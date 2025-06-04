from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

class AdminRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not hasattr(request.user, 'perfil') or not request.user.perfil.es_admin:
            raise PermissionDenied("Acceso restringido a administradores.")
        return super().dispatch(request, *args, **kwargs)

class UserRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not hasattr(request.user, 'perfil') or request.user.perfil.es_admin:
            raise PermissionDenied("Acceso restringido a usuarios.")
        return super().dispatch(request, *args, **kwargs)
