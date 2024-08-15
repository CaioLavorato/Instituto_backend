from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.core.cache import cache
from django.contrib.auth.hashers import check_password
from . import models
from . import forms

# Create your views here.
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            # Encontre o usuário na tabela Usuario
            user = models.Usuario.objects.get(email=email)
        except models.Usuario.DoesNotExist:
            return render(request, 'login.html', {'error': 'Credenciais inválidas'})

        # Verifique a senha
        if check_password(password, user.senha):
            # Autenticar o usuário (não é o mesmo que a autenticação padrão do Django)
            auth_login(request, user)
            # Salvar usuário em cache
            cache.set(f'user_{user.id}', user, timeout=None)
            return redirect('homepage')  # Redireciona para a homepage após o login
        else:
            return render(request, 'login.html', {'error': 'Credenciais inválidas'})

    return render(request, 'login.html')
def homepage(request):
    return render(request, "homepage.html")

def cursos(request):
    return render(request,"cursos.html")

def meuscursos(request):
    return render(request,"meuscursos.html")

def cursodetalhe(request):
    return render(request,"cursodetalhe.html")

def documentos(request):
    return render(request,"documentos.html")

def forumdetalhe(request):
    return render(request,"forumdetalhe.html")

def foruns(request):
    return render(request,"foruns.html")

def perfil(request):
    return render(request,"perfil.html")

def professordetalhe(request):
    return render(request,"professordetalhe.html")

def professores(request):
    return render(request,"professores.html")

def redecredenciada(request):
    return render(request,"redecredenciada.html")

def categorias(request):
    return render(request,"categorias.html")

def categoriadetalhe(request):
    return render(request,"categoriadetalhe.html")

def perfil_view(request):
    if request.method == 'POST':
        form = forms.UsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('perfil')  # Redireciona para a página de perfil após o salvamento
    else:
        form = forms.UsuarioForm()
    return render(request, 'perfil.html', {'form': form})


def criar_forum(request):
    if request.method == 'POST':
        form = forms.ForumForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('criar-forum')  # Substitua pelo nome da sua URL
    else:
        form = forms.ForumForm()

    return render(request, 'novoforum.html', {'form': form})