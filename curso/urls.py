from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', views.login, name='login'),
    path('meus_cursos/', views.meuscursos, name='meus_cursos'),
    path('cursos/', views.cursos, name='cursos'),
    path('cursodetalhe/', views.cursodetalhe, name='cursodetalhe'),
    path('foruns/', views.foruns, name='foruns'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('documentos/', views.documentos, name='documentos'),
    path('professores/', views.professores, name='professores'),
    path('forumdetalhe/', views.forumdetalhe, name='forumdetalhe'),
    path('redecredenciada/', views.redecredenciada, name='redecredenciada'),
    path('professordetalhe/', views.professordetalhe, name='professordetalhe'),
    path('categorias/', views.categorias, name='categorias'),
    path('categoriadetalhe/', views.categoriadetalhe, name='categoriadetalhe'),
    path('criar_forum/', views.criar_forum, name='criar_forum'),
]