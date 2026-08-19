from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.core.exceptions import PermissionDenied

class AdminRequiredMixin(LoginRequiredMixin):
    login_url = 'accounts:login'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role not in {'superadmin','editor','viewer'}: raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
class EditorRequiredMixin(AdminRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'viewer': raise PermissionDenied('Viewer accounts are read-only.')
        return super().dispatch(request, *args, **kwargs)

class StudentRequiredMixin(LoginRequiredMixin):
    login_url = 'student_accounts:login'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role != 'student':
            raise PermissionDenied('Only student accounts can access this section.')
        return super().dispatch(request, *args, **kwargs)
