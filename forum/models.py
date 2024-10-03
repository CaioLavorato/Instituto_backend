from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from curso.models import Curso
from django.core.exceptions import ValidationError
from PIL import Image

def validate_image(image):
    try:
        # Abre o arquivo de imagem
        img = Image.open(image)
        img.verify()  # Verifica se o arquivo é uma imagem
    except Exception as e:
        raise ValidationError('O arquivo não é uma imagem válida. Erro: %s' % e)
    

class TopicoForum(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    conteudo = models.TextField(max_length=3000)
    data_criacao = models.DateTimeField(default=timezone.now)
    thumb = models.ImageField(upload_to='thumb_forum', validators=[validate_image])

    def __str__(self):
        return self.titulo

class RespostaForum(models.Model):
    topico = models.ForeignKey(TopicoForum, on_delete=models.CASCADE, related_name='respostas')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    conteudo = models.TextField(max_length=1000)
    data_criacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Resposta para {self.topico.titulo} por {self.usuario.username}"