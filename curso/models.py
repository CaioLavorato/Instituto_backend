from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.db.models import Avg, Count

class UserProfile(models.Model):
    PROFESSOR = 'PR'
    MEDICO = 'MD'
    ALUNO = 'AL'
    TIPO_USUARIO_CHOICES = [
        (PROFESSOR, 'Professor'),
        (MEDICO, 'Médico'),
        (ALUNO, 'Aluno'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    foto = models.ImageField(upload_to='thumb_usuarios', null=True, blank=True)
    data_de_nascimento = models.DateField(null=True, blank=True)
    facebook = models.CharField(max_length=1000, null=True, blank=True)
    linkedin = models.CharField(max_length=1000, null=True, blank=True)
    google_plus = models.CharField(max_length=1000, null=True, blank=True)
    descricao = models.TextField(max_length=5000, null=True, blank=True)
    web_site = models.CharField(max_length=1000, null=True, blank=True)
    tipo = models.CharField(max_length=2, choices=TIPO_USUARIO_CHOICES, default=ALUNO)
    categorias = models.ManyToManyField('Categorias', related_name='usuarios', blank=True)

    # Campo CPF aceitando pontuações
    cpf = models.CharField(
        max_length=14,  # Permite o tamanho com pontuações
        validators=[RegexValidator(regex='^\d{3}\.\d{3}\.\d{3}-\d{2}$', message='CPF deve ter o formato correto (XXX.XXX.XXX-XX).')],
        unique=True,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.username

# Modelo de Categorias
class Categorias(models.Model):
    descricao = models.TextField(max_length=1000)
    data_criacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.descricao

# Modelo de Curso
class Curso(models.Model):
    titulo = models.CharField(max_length=100)
    thumb = models.ImageField(upload_to='thumb_cursos')
    descricao = models.TextField(max_length=1000)
    categoria = models.ForeignKey('Categorias', on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(default=timezone.now)
    visualizacoes = models.IntegerField(default=0)
    duracao = models.IntegerField(default=0) 
    professor = models.ForeignKey('UserProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name='cursos')

    def __str__(self):
        return self.titulo

    def media_avaliacoes(self):
        return self.avaliacao_set.aggregate(Avg('estrelas'))['estrelas__avg'] or 0

    def num_avaliacoes(self):
        return self.avaliacao_set.count()
    
# Modelo de Modulo
class Modulo(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    ordem = models.IntegerField()

    def __str__(self):
        return self.titulo

# Modelo de Modulo_usuario
class Modulo_usuario(models.Model):
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    ind_concluido = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.usuario.username} - {self.modulo}"

# Modelo de Aula
class Aula(models.Model):
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    conteudo = models.FileField(upload_to='videos_aula')
    ordem = models.IntegerField()

    def __str__(self):
        return self.titulo

# Modelo de Questionario
class Questionario(models.Model):
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.modulo)

# Modelo de Pergunta
class Pergunta(models.Model):
    questionario = models.ForeignKey(Questionario, on_delete=models.CASCADE)
    enunciado = models.CharField(max_length=1000)

    def __str__(self):
        return self.enunciado

# Modelo de Alternativas
class Alternativas(models.Model):
    descricao = models.TextField(max_length=1000)
    resposta_correta = models.BooleanField(default=False)
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)

    def __str__(self):
        return self.descricao

# Modelo de Certificado
class Certificado(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    data_emissao = models.DateTimeField(default=timezone.now)
    codigo = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.usuario.username} - {self.curso}"

# Modelo de Chat
class Chat(models.Model):
    id_remetente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='remetente_chats')
    id_destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='destinatario_chats')
    mensagem = models.TextField(max_length=1000)
    data_envio = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.id_remetente.username} - {self.id_destinatario.username}"


# Modelo de Avaliacao
class Avaliacao(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    estrelas = models.PositiveSmallIntegerField()  # Assumindo que a avaliação é de 1 a 5
    data_criacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.usuario.username} - {self.curso} - {self.estrelas}"
    
# Modelo de Badge
class Badge(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(max_length=1000)
    criterio = models.CharField(max_length=1000)
    icone = models.ImageField(upload_to='badge')
    usuarios = models.ManyToManyField(User, related_name='badges')

    def __str__(self):
        return self.nome

# Modelo de Agendamento
class Agendamento(models.Model):
    id_paciente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agendamentos_paciente')
    id_doutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agendamentos_doutor')
    observacao = models.TextField(max_length=1000)
    data_agendamento = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.id_doutor.username} - {self.data_agendamento}"

# Modelo de LaudosMedicos
class LaudosMedicos(models.Model):
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='laudos_medicos')
    documento = models.FileField()
    observacao = models.TextField(max_length=1000)
    data_inclusao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.documento} - {self.id_usuario.username}"
