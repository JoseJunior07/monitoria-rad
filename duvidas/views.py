from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.db.models import Q
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from django import forms
from functools import wraps
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View

from .models import Disciplina, Duvida


class CadastroView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/cadastro.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)
        grupo_alunos, _ = Group.objects.get_or_create(name="Alunos")
        self.object.groups.add(grupo_alunos)
        return response

def eh_monitor(user):
    return user.groups.filter(name="Monitores").exists()


def eh_professor(user):
    return user.groups.filter(name="Professores").exists()



class DuvidaForm(forms.ModelForm):
    class Meta:
        model = Duvida
        fields = ["titulo", "descricao", "disciplina"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["disciplina"].queryset = Disciplina.objects.filter(ativa=True)


@login_required
def lista_duvidas(request):
    user = request.user
    if eh_professor(user):
        duvidas = Duvida.objects.all()
    elif eh_monitor(user):
        duvidas = Duvida.objects.filter(disciplina__monitores=user)
    else:
        duvidas = Duvida.objects.filter(autor=user)
    return render(request, "duvidas/lista_duvidas.html", {"duvidas": duvidas})


@login_required
def abrir_duvida(request):
    if request.method == "POST":
        form = DuvidaForm(request.POST)
        if form.is_valid():
            duvida = form.save(commit=False)
            duvida.autor = request.user
            duvida.situacao = Duvida.Situacao.ABERTA
            duvida.save()
            return redirect("lista_duvidas")
    else:
        form = DuvidaForm()
    return render(request, "duvidas/abrir_duvida.html", {"form": form})

def monitor_da_disciplina_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        duvida = get_object_or_404(Duvida, pk=kwargs["pk"])
        if not duvida.disciplina.monitores.filter(pk=request.user.pk).exists():
            return HttpResponseForbidden("Você não é monitor desta disciplina.")
        request.duvida = duvida
        return view_func(request, *args, **kwargs)
    return wrapper

class ApenasAutorMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        self.duvida = get_object_or_404(Duvida, pk=kwargs["pk"])
        if self.duvida.autor_id != request.user.pk:
            return HttpResponseForbidden("Apenas o autor pode fazer isso.")
        return super().dispatch(request, *args, **kwargs)
    
@monitor_da_disciplina_required
def assumir_duvida(request, pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    duvida = request.duvida
    if duvida.situacao != Duvida.Situacao.ABERTA:
        return HttpResponseForbidden("Esta dúvida já foi assumida.")
    duvida.monitor_responsavel = request.user
    duvida.situacao = Duvida.Situacao.EM_ATENDIMENTO
    duvida.save()
    return redirect("lista_duvidas")


@login_required
def responder_duvida(request, pk):
    duvida = get_object_or_404(Duvida, pk=pk)
    if duvida.monitor_responsavel_id != request.user.pk:
        return HttpResponseForbidden("Apenas o monitor responsável pode responder.")
    if request.method == "POST":
        resposta = request.POST.get("resposta", "").strip()
        if not resposta:
            messages.error(request, "A resposta não pode ficar em branco.")
            return redirect("lista_duvidas")
        duvida.resposta = resposta
        duvida.situacao = Duvida.Situacao.RESPONDIDA
        duvida.save()
    return redirect("lista_duvidas")


class EncerrarDuvidaView(ApenasAutorMixin, View):
    def post(self, request, pk):
        duvida = self.duvida
        if not duvida.resposta:
            return HttpResponseForbidden("Só é possível encerrar dúvida com resposta.")
        duvida.situacao = Duvida.Situacao.ENCERRADA
        duvida.save()
        return redirect("lista_duvidas")
    
@login_required
def base_conhecimento(request):
    termo = request.GET.get("q", "")
    duvidas = Duvida.objects.filter(
        situacao__in=[Duvida.Situacao.RESPONDIDA, Duvida.Situacao.ENCERRADA]
    )
    if termo:
        duvidas = duvidas.filter(
            Q(titulo__icontains=termo) | Q(descricao__icontains=termo)
        )
    return render(request, "duvidas/base_conhecimento.html", {"duvidas": duvidas, "termo": termo})