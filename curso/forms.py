from django import forms
from .models import Usuario, Agendamento, Forum


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'  # Inclua todos os campos do modelo

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)

        # Escondendo os campos "senha" e "tipo" por padrão
        self.fields['senha'].widget = forms.HiddenInput()
        self.fields['tipo'].widget = forms.HiddenInput()

        if 'tipo' in self.data:
            tipo = self.data.get('tipo')
        elif self.instance.pk:
            tipo = self.instance.tipo
        else:
            tipo = Usuario.ALUNO

        if tipo == Usuario.PROFESSOR:
            # Se o tipo for "Professor", exibe todos os campos exceto "senha" e "tipo"
            self.fields['senha'].widget = forms.HiddenInput()
            self.fields['tipo'].widget = forms.HiddenInput()
        elif tipo == Usuario.ALUNO:
            # Se o tipo for "Aluno", esconde o campo "tipo"
            self.fields['tipo'].widget = forms.HiddenInput()
        else:
            # Outras lógicas para outros tipos de usuários, se necessário
            pass


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