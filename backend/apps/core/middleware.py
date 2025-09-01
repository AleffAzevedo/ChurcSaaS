from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
from .models import Igreja


class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/admin/') or request.path.startswith('/api/auth/'):
            return None
            
        if hasattr(request, 'user') and request.user.is_authenticated:
            if hasattr(request.user, 'igreja'):
                request.tenant = request.user.igreja
            else:
                return HttpResponseForbidden("Usuário não associado a uma igreja")
        
        return None
