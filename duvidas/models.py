from django.conf import settings
from django.db import models


class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, unique=True)
    ativa = models.BooleanField(default=True)
    monitores = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="disciplinas_monitoradas",
        blank=True,
    )

    class Meta:
        ordering = ["nome"]
        verbose_name = "Disciplina"
        verbose_name_plural = "Disciplinas"

    def __str__(self):
        return f"{self.nome} ({self.codigo})"


class Duvida(models.Model):
    class Situacao(models.TextChoices):
        ABERTA = "AB", "Aberta"
        EM_ATENDIMENTO = "EA", "Em atendimento"
        RESPONDIDA = "RE", "Respondida"
        ENCERRADA = "EN", "Encerrada"

    titulo = models.CharField(max_length=150)
    descricao = models.TextField()
    disciplina = models.ForeignKey(
        Disciplina, on_delete=models.PROTECT, related_name="duvidas"
    )
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="duvidas_abertas",
    )
    monitor_responsavel = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="duvidas_atendidas",
        null=True,
        blank=True,
    )
    resposta = models.TextField(blank=True)
    situacao = models.CharField(
        max_length=2, choices=Situacao.choices, default=Situacao.ABERTA
    )
    aberta_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-aberta_em"]
        verbose_name = "Dúvida"
        verbose_name_plural = "Dúvidas"

    def __str__(self):
        return self.titulo
