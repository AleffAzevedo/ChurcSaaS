from rest_framework import permissions
from .models import NivelOrganizacional


class IsTenantUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'igreja') and
            request.user.igreja.ativa
        )


class HasPermission(permissions.BasePermission):
    def __init__(self, permission_code, action='read'):
        self.permission_code = permission_code
        self.action = action

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
            
        if request.user.is_superuser:
            return True
            
        user_permissions = self._get_user_permissions(request.user)
        
        if self.permission_code not in user_permissions:
            return False
            
        permission = user_permissions[self.permission_code]
        
        action_map = {
            'GET': 'pode_ler',
            'POST': 'pode_criar',
            'PUT': 'pode_editar',
            'PATCH': 'pode_editar',
            'DELETE': 'pode_excluir',
        }
        
        required_permission = action_map.get(request.method, 'pode_ler')
        return getattr(permission, required_permission, False)

    def _get_user_permissions(self, user):
        permissions = {}
        
        for papel_usuario in user.usuariopapel_set.filter(
            data_inicio__lte=timezone.now().date(),
            data_fim__isnull=True
        ):
            for papel_permissao in papel_usuario.papel.papelpermissao_set.all():
                code = papel_permissao.permissao.codigo
                if code not in permissions:
                    permissions[code] = papel_permissao
                else:
                    existing = permissions[code]
                    permissions[code] = self._merge_permissions(existing, papel_permissao)
        
        return permissions

    def _merge_permissions(self, perm1, perm2):
        return type('Permission', (), {
            'pode_ler': perm1.pode_ler or perm2.pode_ler,
            'pode_criar': perm1.pode_criar or perm2.pode_criar,
            'pode_editar': perm1.pode_editar or perm2.pode_editar,
            'pode_excluir': perm1.pode_excluir or perm2.pode_excluir,
            'pode_aprovar': perm1.pode_aprovar or perm2.pode_aprovar,
        })()


class IsMatrizLevel(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.nivel_acesso == NivelOrganizacional.MATRIZ
        )


class IsSetorialOrAbove(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.nivel_acesso in [NivelOrganizacional.MATRIZ, NivelOrganizacional.SETORIAL]
        )
