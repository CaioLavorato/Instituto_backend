from django import forms
from .models import Usuario, Agendamento, Forum


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)

        # Verificar se o formulário está sendo usado no Django Admin
        if not kwargs.get('instance', None):
            # Campos que devem ser sempre ocultos fora do Admin
            campos_ocultos = ['data_criacao', 'ultimo_acesso', 'senha']
            for campo in campos_ocultos:
                if campo in self.fields:
                    self.fields[campo].widget = forms.HiddenInput()

            # Campos específicos para o tipo "Professor"
            campos_professor = ['categorias', 'web_site', 'descricao', 'google_plus', 'linkedin', 'facebook']

            # Esconde todos os campos relacionados ao professor por padrão fora do Admin
            for campo in campos_professor:
                if campo in self.fields:
                    self.fields[campo].widget = forms.HiddenInput()

            # Verifica o tipo de usuário
            if 'tipo' in self.data:
                tipo = self.data.get('tipo')
            elif self.instance.pk:
                tipo = self.instance.tipo
            else:
                tipo = Usuario.ALUNO

            # Se o tipo for "Professor", exibe os campos relacionados ao professor
            if tipo == Usuario.PROFESSOR:
                for campo in campos_professor:
                    if campo in self.fields:
                        self.fields[campo].widget = forms.TextInput()  # Ou outro widget apropriado
            else:
                if 'tipo' in self.fields:
                    self.fields['tipo'].widget = forms.HiddenInput()

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = '__all__'
        labels = {
            'id_paciente': 'Paciente',
            'id_doutor': 'Doutor',
        }

class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ['curso', 'usuario', 'titulo', 'conteudo']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o título do fórum'}),
            'conteudo': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Escreva o conteúdo do fórum'}),
        }