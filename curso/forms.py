from django import forms
from .models import Usuario,Agendamento

class UsuarioForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = '__all__'

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = '__all__'
        labels = {
            'id_paciente': 'Paciente',
            'id_doutor': 'Doutor',
        }