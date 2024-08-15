from django import forms
from .models import Usuario, Agendamento, Forum

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'cpf', 'email', 'senha', 'foto', 'data_de_nascimento', 'ultimo_acesso', 'tipo']
        widgets = {
            'senha': forms.PasswordInput(),
            'data_de_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'ultimo_acesso': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

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