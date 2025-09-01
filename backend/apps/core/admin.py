from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Igreja, Campus, User, Papel, Permissao, PapelPermissao, UsuarioPapel, LogAuditoria


@admin.register(Igreja)
class IgrejaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cnpj', 'plano', 'ativa', 'created_at']
    list_filter = ['plano', 'ativa', 'created_at']
    search_fields = ['nome', 'cnpj', 'email']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Campus)
class CampusAdmin(admin.ModelAdmin):
    list_display = ['nome', 'igreja', 'nivel', 'campus_pai', 'is_active']
    list_filter = ['nivel', 'igreja', 'is_active']
    search_fields = ['nome', 'igreja__nome']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'igreja', 'nivel_acesso', 'is_active']
    list_filter = ['nivel_acesso', 'igreja', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    readonly_fields = ['id', 'date_joined', 'last_login', 'data_aceite_lgpd']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informações da Igreja', {
            'fields': ('igreja', 'campus', 'nivel_acesso', 'scope_ids')
        }),
        ('Informações Pessoais Extras', {
            'fields': ('telefone', 'foto')
        }),
        ('LGPD', {
            'fields': ('aceite_termos', 'aceite_lgpd', 'data_aceite_lgpd')
        }),
    )


@admin.register(Papel)
class PapelAdmin(admin.ModelAdmin):
    list_display = ['nome', 'igreja', 'nivel_minimo', 'is_active']
    list_filter = ['nivel_minimo', 'igreja', 'is_active']
    search_fields = ['nome', 'descricao']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Permissao)
class PermissaoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'codigo', 'modulo', 'is_active']
    list_filter = ['modulo', 'is_active']
    search_fields = ['nome', 'codigo', 'descricao']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(PapelPermissao)
class PapelPermissaoAdmin(admin.ModelAdmin):
    list_display = ['papel', 'permissao', 'pode_ler', 'pode_criar', 'pode_editar', 'pode_excluir']
    list_filter = ['papel__igreja', 'permissao__modulo']
    search_fields = ['papel__nome', 'permissao__nome']


@admin.register(UsuarioPapel)
class UsuarioPapelAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'papel', 'campus', 'data_inicio', 'data_fim']
    list_filter = ['papel', 'campus', 'data_inicio']
    search_fields = ['usuario__username', 'papel__nome']


@admin.register(LogAuditoria)
class LogAuditoriaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'acao', 'modelo', 'objeto_id', 'created_at']
    list_filter = ['acao', 'modelo', 'created_at', 'igreja']
    search_fields = ['usuario__username', 'modelo', 'objeto_id']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
