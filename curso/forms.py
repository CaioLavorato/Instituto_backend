from django import forms
from .models import UserProfile, Agendamento
from django.core.exceptions import ValidationError
import re

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['cpf', 'foto', 'data_de_nascimento', 'facebook', 'linkedin', 'google_plus', 'descricao', 'web_site', 'categorias']
        
        widgets = {
            'data_de_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'facebook': forms.URLInput(attrs={'class': 'form-control'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control'}),
            'google_plus': forms.URLInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'web_site': forms.URLInput(attrs={'class': 'form-control'}),
            'categorias': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

        # Esconde o campo 'tipo' se ele existir no formulário
        if 'tipo' in self.fields:
            self.fields['tipo'].widget = forms.HiddenInput()

        # Verifica se o formulário está sendo usado para criar ou editar um perfil existente
        user_profile_instance = kwargs.get('instance', None)

        # Se existe um perfil, segue as regras específicas
        if user_profile_instance:
            campos_professor = ['categorias', 'web_site', 'descricao', 'google_plus', 'linkedin', 'facebook']
            
            # Esconde todos os campos de professor por padrão
            for campo in campos_professor:
                if campo in self.fields:
                    self.fields[campo].widget = forms.HiddenInput()
            
            # Exibe os campos de professor se o tipo for "Professor"
            if user_profile_instance.tipo == UserProfile.PROFESSOR:
                for campo in campos_professor:
                    if campo in self.fields:
                        self.fields[campo].widget = self.fields[campo].widget.__class__(attrs={'class': 'form-control'})

    def clean_data_de_nascimento(self):
        data_de_nascimento = self.cleaned_data.get('data_de_nascimento')
        if data_de_nascimento:
            # Certifique-se de que a data está no formato correto
            return data_de_nascimento
        raise forms.ValidationError("Data de nascimento inválida.")
    
    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf', '')
        # Remove todas as pontuações para validação
        cpf_clean = re.sub(r'\D', '', cpf)
        # Verifica se o CPF contém exatamente 11 dígitos
        if len(cpf_clean) != 11:
            raise ValidationError('CPF deve conter exatamente 11 dígitos.')
        # Formata o CPF para armazenar com pontuações
        cpf_formatted = f"{cpf_clean[:3]}.{cpf_clean[3:6]}.{cpf_clean[6:9]}-{cpf_clean[9:]}"
        return cpf_formatted



class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = '__all__'
        labels = {
            'id_paciente': 'Paciente',
            'id_doutor': 'Doutor',
        }


class LoginForm(forms.Form):
    email = forms.CharField(max_length=100)
    senha = forms.CharField(widget=forms.PasswordInput)