from django.shortcuts import render, redirect
from . import forms

# Create your views here.
def login(request):
    return render(request, "login.html")
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