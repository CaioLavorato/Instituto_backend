# api/views.py
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from curso.models import UserProfile, Curso, Modulo, Aula, Questionario, Pergunta, Alternativas, Certificado, Chat, Avaliacao, Badge, Agendamento, LaudosMedicos
from .serializers import UserSerializer, UserProfileSerializer, CursoSerializer, ModuloSerializer, AulaSerializer, \
    QuestionarioSerializer, PerguntaSerializer, AlternativasSerializer, CertificadoSerializer, ChatSerializer, AvaliacaoSerializer, BadgeSerializer, AgendamentoSerializer, LaudosMedicosSerializer, \
    UserRegistrationSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CursoDetailSerializer
        return CursoSerializer

    @action(detail=True, methods=['get'])
    def modulos(self, request, pk=None):
        curso = self.get_object()
        modulos = curso.modulos.all()
        serializer = ModuloNestedSerializer(modulos, many=True)
        return Response(serializer.data)

class ModuloViewSet(viewsets.ModelViewSet):
    queryset = Modulo.objects.all()
    serializer_class = ModuloSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ModuloDetailSerializer
        return ModuloSerializer

    @action(detail=True, methods=['get'])
    def aulas(self, request, pk=None):
        modulo = self.get_object()
        aulas = modulo.aulas.all()
        serializer = AulaNestedSerializer(aulas, many=True)
        return Response(serializer.data)

class AulaViewSet(viewsets.ModelViewSet):
    queryset = Aula.objects.all()
    serializer_class = AulaSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AulaDetailSerializer
        return AulaSerializer

class QuestionarioViewSet(viewsets.ModelViewSet):
    queryset = Questionario.objects.all()
    serializer_class = QuestionarioSerializer
    permission_classes = [IsAuthenticated]

class PerguntaViewSet(viewsets.ModelViewSet):
    queryset = Pergunta.objects.all()
    serializer_class = PerguntaSerializer
    permission_classes = [IsAuthenticated]

class AlternativasViewSet(viewsets.ModelViewSet):
    queryset = Alternativas.objects.all()
    serializer_class = AlternativasSerializer
    permission_classes = [IsAuthenticated]

class CertificadoViewSet(viewsets.ModelViewSet):
    queryset = Certificado.objects.all()
    serializer_class = CertificadoSerializer
    permission_classes = [IsAuthenticated]

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

class AvaliacaoViewSet(viewsets.ModelViewSet):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer
    permission_classes = [IsAuthenticated]

class BadgeViewSet(viewsets.ModelViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    permission_classes = [IsAuthenticated]

class AgendamentoViewSet(viewsets.ModelViewSet):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
    permission_classes = [IsAuthenticated]

class LaudosMedicosViewSet(viewsets.ModelViewSet):
    queryset = LaudosMedicos.objects.all()
    serializer_class = LaudosMedicosSerializer
    permission_classes = [IsAuthenticated]


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class UserRegistrationView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer