from django.contrib import admin
from .models import Disciplina, Duvida


@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ("nome", "codigo", "ativa")
    list_filter = ("ativa",)
    search_fields = ("nome", "codigo")
    filter_horizontal = ("monitores",)


@admin.register(Duvida)
class DuvidaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "disciplina", "autor", "monitor_responsavel", "situacao")
    list_filter = ("situacao", "disciplina")
    search_fields = ("titulo", "descricao")
