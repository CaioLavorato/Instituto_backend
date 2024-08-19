# api/urls.py
from django.urls import path, include
from .views import CustomAuthToken, UserRegistrationView
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserProfileViewSet, CursoViewSet, ModuloViewSet, AulaViewSet, QuestionarioViewSet, PerguntaViewSet, AlternativasViewSet, CertificadoViewSet, ChatViewSet, ForumViewSet, AvaliacaoViewSet, BadgeViewSet, AgendamentoViewSet, LaudosMedicosViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', UserProfileViewSet)
router.register(r'cursos', CursoViewSet)
router.register(r'modulos', ModuloViewSet)
router.register(r'aulas', AulaViewSet)
router.register(r'questionarios', QuestionarioViewSet)
router.register(r'perguntas', PerguntaViewSet)
router.register(r'alternativas', AlternativasViewSet)
router.register(r'certificados', CertificadoViewSet)
router.register(r'chats', ChatViewSet)
router.register(r'forums', ForumViewSet)
router.register(r'avaliacoes', AvaliacaoViewSet)
router.register(r'badges', BadgeViewSet)
router.register(r'agendamentos', AgendamentoViewSet)
router.register(r'laudos', LaudosMedicosViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('login/', CustomAuthToken.as_view(), name='api_login'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
]