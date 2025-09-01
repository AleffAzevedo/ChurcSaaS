from django.contrib import admin
from .models import Grupo, MembroGrupo, Reuniao, PresencaReuniao, MaterialEstudo, GrupoMaterial


@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo', 'campus', 'lider', 'total_membros', 'meta_membros', 'is_active']
    list_filter = ['tipo', 'campus', 'dia_reuniao', 'is_active']
    search_fields = ['nome', 'descricao', 'endereco']
    readonly_fields = ['id', 'created_at', 'updated_at', 'total_membros', 'percentual_meta']


@admin.register(MembroGrupo)
class MembroGrupoAdmin(admin.ModelAdmin):
    list_display = ['pessoa', 'grupo', 'status', 'data_entrada', 'data_saida']
    list_filter = ['status', 'grupo', 'data_entrada']
    search_fields = ['pessoa__nome_completo', 'grupo__nome']


@admin.register(Reuniao)
class ReuniaoAdmin(admin.ModelAdmin):
    list_display = ['grupo', 'data_reuniao', 'tema', 'total_presentes', 'total_visitantes', 'total_conversoes']
    list_filter = ['grupo', 'data_reuniao', 'responsavel']
    search_fields = ['tema', 'versiculo', 'grupo__nome']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(PresencaReuniao)
class PresencaReuniaoAdmin(admin.ModelAdmin):
    list_display = ['pessoa', 'reuniao', 'presente', 'visitante']
    list_filter = ['presente', 'visitante', 'reuniao__grupo']
    search_fields = ['pessoa__nome_completo', 'reuniao__tema']


@admin.register(MaterialEstudo)
class MaterialEstudoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'categoria', 'autor', 'data_publicacao', 'is_active']
    list_filter = ['categoria', 'data_publicacao', 'is_active']
    search_fields = ['titulo', 'descricao', 'autor']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(GrupoMaterial)
class GrupoMaterialAdmin(admin.ModelAdmin):
    list_display = ['grupo', 'material', 'data_inicio', 'data_fim']
    list_filter = ['grupo', 'data_inicio']
    search_fields = ['grupo__nome', 'material__titulo']
