from django.urls import path
from . import views

urlpatterns = [
    path("cadastro/", views.CadastroView.as_view(), name="cadastro"),
    path("duvidas/", views.lista_duvidas, name="lista_duvidas"),
    path("duvidas/abrir/", views.abrir_duvida, name="abrir_duvida"),
    path("duvidas/<int:pk>/assumir/", views.assumir_duvida, name="assumir_duvida"),
    path("duvidas/<int:pk>/responder/", views.responder_duvida, name="responder_duvida"),
    path("duvidas/<int:pk>/encerrar/", views.EncerrarDuvidaView.as_view(), name="encerrar_duvida"),
    path("base-conhecimento/", views.base_conhecimento, name="base_conhecimento"),
]