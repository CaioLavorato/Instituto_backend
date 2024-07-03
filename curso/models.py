from django.db import models
from django.utils import timezone

# Create your models here.

CATEGORIAS = (
    ("categoria1", "Categoria 1"),
    ("categoria2", "Categoria 2"),
    ("categoria3", "Categoria 3")
)

class Curso(models.Model):
    titulo = models.CharField(max_length=100)
    thumb = models.ImageField(upload_to='thumb_cursos')
    descricao = models.TextField(max_length=1000)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    data_criacao = models.DateTimeField(default=timezone.now)
    visualizacoes = models.IntegerField(default=0)

    def __str__(self):
        return self.titulo

    #titulo, descricao, categoria, data_de_criacao, visualizacoes