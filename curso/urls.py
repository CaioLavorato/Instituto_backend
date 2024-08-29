from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', views.login_view, name='login'),
    path('meus_cursos/', views.meuscursos, name='meus_cursos'),
    path('cursos/', views.cursos, name='cursos'),
    path('cursodetalhe/', views.cursodetalhe, name='cursodetalhe'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('documentos/', views.documentos, name='documentos'),
    path('professores/', views.professores, name='professores'),
    path('redecredenciada/', views.redecredenciada, name='redecredenciada'),
    path('professordetalhe/', views.professordetalhe, name='professordetalhe'),
    path('categorias/', views.categorias, name='categorias'),
    path('categoriadetalhe/', views.categoriadetalhe, name='categoriadetalhe'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('foruns/', views.foruns,name='foruns'),
    path('criar_forum/', views.criar_forum,name='criar_forum'),
    path('forumdetalhe/', views.forumdetalhe,name='forumdetalhe')
]