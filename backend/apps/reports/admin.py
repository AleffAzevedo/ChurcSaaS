from django.contrib import admin
from .models import RelatorioPersonalizado, ExecucaoRelatorio, Dashboard, Widget


@admin.register(RelatorioPersonalizado)
class RelatorioPersonalizadoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo', 'publico', 'criado_por', 'is_active']
    list_filter = ['tipo', 'publico', 'is_active']
    search_fields = ['nome', 'descricao']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(ExecucaoRelatorio)
class ExecucaoRelatorioAdmin(admin.ModelAdmin):
    list_display = ['relatorio', 'usuario', 'data_execucao', 'status', 'total_registros', 'tempo_execucao']
    list_filter = ['status', 'data_execucao', 'relatorio']
    search_fields = ['relatorio__nome', 'usuario__username']
    readonly_fields = ['data_execucao', 'created_at', 'updated_at']


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ['nome', 'publico', 'padrao', 'criado_por', 'is_active']
    list_filter = ['publico', 'padrao', 'is_active']
    search_fields = ['nome', 'descricao']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Widget)
class WidgetAdmin(admin.ModelAdmin):
    list_display = ['nome', 'dashboard', 'tipo', 'posicao_x', 'posicao_y', 'largura', 'altura']
    list_filter = ['tipo', 'dashboard', 'atualizar_automatico']
    search_fields = ['nome', 'dashboard__nome']
    readonly_fields = ['id', 'created_at', 'updated_at']
