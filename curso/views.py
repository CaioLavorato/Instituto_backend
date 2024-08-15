from django.shortcuts import render

# Create your views here.
def homepage(request):
    return render(request, "homepage.html")

def cursos(request):
    return render(request,"cursos.html")

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
