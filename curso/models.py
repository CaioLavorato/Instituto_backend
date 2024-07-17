from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password


# Create your models here.

class Usuario(models.Model):
    nome = models.CharField(max_length=1000)
    cpf = models.CharField(max_length=11)
    email = models.CharField(max_length=100)
    senha = models.CharField(max_length=128)
    foto = models.ImageField(upload_to='thumb_usuarios')
    data_de_nascimento = models.DateTimeField()
    data_criacao = models.DateTimeField(default=timezone.now)
    ultimo_acesso = models.DateTimeField()

    def __str__(self):
        return self.nome


# nome, cpf, email, senha, foto, data_de_nascimento, data_de_criacao, ultimo_acesso

class Categorias(models.Model):
    descricao = models.TextField(max_length=1000)
    data_criacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.descricao


# descricao, data_criacao

class Curso(models.Model):
    titulo = models.CharField(max_length=100)
    thumb = models.ImageField(upload_to='thumb_cursos')
    descricao = models.TextField(max_length=1000)
    categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(default=timezone.now)
    visualizacoes = models.IntegerField(default=0)

    def __str__(self):
        return self.titulo


# titulo, descricao, categoria, data_de_criacao, visualizacoes

class Modulo(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    ordem = models.IntegerField()

    def __str__(self):
        return self.titulo


# id, curso_id, titulo, ordem

class Modulo_usuario(models.Model):
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    ind_concluido = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.usuario} - {self.modulo}"


# modulo,usuario,ind_concluido

class Aula(models.Model):
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    conteudo = models.FileField(upload_to='videos_aula')
    ordem = models.IntegerField()

    def __str__(self):
        return self.titulo


# modulo_id, titulo, conteudo, ordem
class Questionario(models.Model):
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)

    def __str__(self):
        return self.modulo


# modulo_id
class Pergunta(models.Model):
    questionario = models.ForeignKey(Questionario, on_delete=models.CASCADE)
    enunciado = models.CharField(max_length=1000)

    def __str__(self):
        return self.enunciado


# questionario_id, enunciado
class Alternativas(models.Model):
    descricao = models.TextField(max_length=1000)
    resposta_correta = models.BooleanField(default=False)
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)

    def __str__(self):
        return self.descricao


class Certificado(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    data_emissao = models.DateTimeField()
    codigo = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.usuario} - {self.curso}"


# usuario_id, curso_id, data_de_emissao, codigo
class Chat(models.Model):
    id_remetente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='remetente_chats')
    id_destinatario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='destinatario_chats')
    mensagem = models.TextField(max_length=1000)
    data_envio = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.id_remetente} - {self.id_destinatario}"


# usuario_remetente,usuario_destinatario,mensagem,data_envio
class Forum(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    conteudo = models.TextField(max_length=3000)
    data_criacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titulo


# curso_id, usuario_id, titulo, conteudo, data_criacao.
class Avaliacao(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    estrelas = models.IntegerField()
    data_criacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.usuario} - {self.curso} - {self.estrelas}"


# curso,usuario,estrelas,data_criacao

class Badge(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(max_length=1000)
    criterio = models.CharField(max_length=1000)
    icone = models.ImageField(upload_to='badge')
    usuarios = models.ManyToManyField(Usuario, related_name='badges')

    def __str__(self):
        return self.nome


# nome,descricao,criterio,icone,usuarios
class Agendamento(models.Model):
    id_paciente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='agendamentos_paciente')
    id_doutor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='agendamentos_doutor')
    observacao = models.TextField(max_length=1000)
    data_agendamento = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.id_doutor} - {self.data_agendamento}"


class LaudosMedicos(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='laudos_medicos')
    documento = models.FileField()
    observacao = models.TextField(max_length=1000)
    data_inclusao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.documento} - {self.id_usuario}"

