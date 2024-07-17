from django.contrib import admin

# Register your models here.
from .models import Curso,Usuario,Modulo_usuario,Modulo,Categorias,Questionario,Aula,Chat,Badge,Forum,Avaliacao,Pergunta,Certificado,Alternativas,LaudosMedicos,Agendamento

admin.site.register(Curso)
admin.site.register(Usuario)
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
admin.site.register(Agendamento)
