# api/urls.py
from django.urls import path, include
from .views import CustomAuthToken, UserRegistrationView
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import UserViewSet, UserProfileViewSet, CursoViewSet, ModuloViewSet, AulaViewSet, QuestionarioViewSet, PerguntaViewSet, AlternativasViewSet, CertificadoViewSet, ChatViewSet, AvaliacaoViewSet, BadgeViewSet, AgendamentoViewSet, LaudosMedicosViewSet

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
router.register(r'avaliacoes', AvaliacaoViewSet)
router.register(r'badges', BadgeViewSet)
router.register(r'agendamentos', AgendamentoViewSet)
router.register(r'laudos', LaudosMedicosViewSet)

nested_urlpatterns = [
    path('cursos/<int:curso_pk>/modulos/', 
         ModuloViewSet.as_view({'get': 'list'}), 
         name='curso-modulos-list'),
    path('cursos/<int:curso_pk>/modulos/<int:pk>/', 
         ModuloViewSet.as_view({'get': 'retrieve'}), 
         name='curso-modulos-detail'),
    path('modulos/<int:modulo_pk>/aulas/', 
         AulaViewSet.as_view({'get': 'list'}), 
         name='modulo-aulas-list'),
    path('modulos/<int:modulo_pk>/aulas/<int:pk>/', 
         AulaViewSet.as_view({'get': 'retrieve'}), 
         name='modulo-aulas-detail'),
]

urlpatterns = [
    path('', include(router.urls)),
    path('', include(nested_urlpatterns)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('login/', CustomAuthToken.as_view(), name='api_login'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
]