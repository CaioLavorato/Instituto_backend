from django.urls import path
from .views import homepage, cursos, cursodetalhe, foruns, perfil, documentos, professores, forumdetalhe, redecredenciada, professordetalhe, categorias,categoriadetalhe

urlpatterns = [
    path('', homepage, name='homepage'),
    path('cursos/', cursos, name='cursos'),
    path('cursodetalhe/', cursodetalhe, name='cursodetalhe'),
    path('foruns/', foruns, name='foruns'),
    path('perfil/', perfil, name='perfil'),
    path('documentos/', documentos, name='documentos'),
    path('professores/', professores, name='professores'),
    path('forumdetalhe/', forumdetalhe, name='forumdetalhe'),
    path('redecredenciada/', redecredenciada, name='redecredenciada'),
    path('professordetalhe/', professordetalhe, name='professordetalhe'),
    path('categorias/', categorias, name='categorias'),
    path('categoriadetalhe/', categoriadetalhe, name='categoriadetalhe'),
]