from django import forms
from .models import TopicoForum, RespostaForum

class FormularioTopico(forms.ModelForm):
    class Meta:
        model = TopicoForum
        fields = ['curso', 'aula' ,'titulo', 'conteudo', 'thumb']

class FormularioResposta(forms.ModelForm):
    class Meta:
        model = RespostaForum
        fields = ['conteudo']