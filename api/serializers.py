# api/serializers.py
import re
from rest_framework import serializers
from django.contrib.auth.models import User
from curso.models import UserProfile, Curso, Modulo, Aula, Questionario, Pergunta, Alternativas, Certificado, Chat, Forum, \
    Avaliacao, Badge, Agendamento, LaudosMedicos


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    first_name = serializers.CharField(max_length=150)  # Substituindo 'nome' por 'first_name'
    last_name = serializers.CharField(max_length=150)  # Adicionando 'last_name' para o sobrenome
    cpf = serializers.CharField(max_length=14)
    email = serializers.EmailField()
    senha = serializers.CharField(write_only=True)
    data_de_nascimento = serializers.DateField()
    tipo = serializers.CharField(max_length=10)

    def validate_cpf(self, value):
        cpf = re.sub(r'[^0-9]', '', value)

        # Verifica se o CPF tem 11 dígitos
        if len(cpf) != 11:
            raise serializers.ValidationError("CPF deve conter 11 dígitos numéricos.")

        return cpf

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este nome de usuário já está em uso.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email já está em uso.")
        return value

    def create(self, validated_data):
        nome_completo = validated_data.pop('nome').split(' ')
        first_name = nome_completo[0]
        last_name = ' '.join(nome_completo[1:])
        user = User.objects.create(
            username=validated_data['username'],
            first_name=first_name,
            last_name=last_name,
            email=validated_data['email']
        )
        UserProfile.objects.create(
            user=user,
            cpf=validated_data['cpf'],
            data_de_nascimento=validated_data['data_de_nascimento'],
            tipo=UserProfile.ALUNO  # Definindo o tipo padrão como ALUNO
        )
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'


class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'


class ModuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modulo
        fields = '__all__'


class AulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aula
        fields = '__all__'


class QuestionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionario
        fields = '__all__'


class PerguntaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pergunta
        fields = '__all__'


class AlternativasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alternativas
        fields = '__all__'


class CertificadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificado
        fields = '__all__'


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'


class ForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum
        fields = '__all__'


class AvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaliacao
        fields = '__all__'


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = '__all__'


class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = '__all__'


class LaudosMedicosSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaudosMedicos
        fields = '__all__'