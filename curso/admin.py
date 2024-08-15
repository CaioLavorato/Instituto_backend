from django.contrib import admin
from .models import (
    Curso, Usuario, Modulo_usuario, Modulo, Categorias, Questionario,
    Aula, Chat, Badge, Forum, Avaliacao, Pergunta, Certificado,
    Alternativas, LaudosMedicos, Agendamento
)
from .forms import UsuarioForm, AgendamentoForm

class UsuarioAdmin(admin.ModelAdmin):
    form = UsuarioForm

    # Lista de campos a serem exibidos no formulário do admin
    fields = [
        'nome', 'cpf', 'email', 'senha', 'foto', 'data_de_nascimento',
        'data_criacao', 'ultimo_acesso', 'tipo', 'facebook',
        'linkedin', 'google_plus', 'descricao', 'web_site', 'categorias'
    ]

    list_display = ['nome', 'email', 'tipo', 'data_criacao']
    list_filter = ['tipo', 'data_criacao']
    search_fields = ['nome', 'email']





class AgendamentoAdmin(admin.ModelAdmin):
    form = AgendamentoForm

admin.site.register(Agendamento, AgendamentoAdmin)
admin.site.register(Curso)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Modulo_usuario)
admin.site.register(Modulo)
admin.site.register(Categorias)
admin.site.register(Questionario)
admin.site.register(Aula)
admin.site.register(Chat)
admin.site.register(Badge)
admin.site.register(Forum)
admin.site.register(Avaliacao)
admin.site.register(Pergunta)
admin.site.register(Certificado)
admin.site.register(Alternativas)
admin.site.register(LaudosMedicos)
