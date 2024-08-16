from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from . import forms

User = get_user_model()  # Obtém o modelo de usuário configurado

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        
        if not email or not senha:
            messages.error(request, 'Por favor, preencha todos os campos.')
            return render(request, 'login.html')
        
        # Autenticar usuário usando email e senha
        user = authenticate(request, username=email, password=senha)
        if user is not None:
            # Autenticação bem-sucedida
            auth_login(request, user)
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('cursos')
        else:
            messages.error(request, 'Credenciais inválidas. Por favor, tente novamente.')
    
    return render(request, 'login.html')


def homepage(request):
    return render(request, "homepage.html")

@login_required
def cursos(request):
    return render(request,"cursos.html")

@login_required
def meuscursos(request):
    return render(request,"meuscursos.html")

@login_required
def cursodetalhe(request):
    return render(request,"cursodetalhe.html")

@login_required
def documentos(request):
    return render(request,"documentos.html")

@login_required
def forumdetalhe(request):
    return render(request,"forumdetalhe.html")

@login_required
def foruns(request):
    return render(request,"foruns.html")

@login_required
def perfil(request):
    return render(request,"perfil.html")

@login_required
def professordetalhe(request):
    return render(request,"professordetalhe.html")

@login_required
def professores(request):
    return render(request,"professores.html")

@login_required
def redecredenciada(request):
    return render(request,"redecredenciada.html")

@login_required
def categorias(request):
    return render(request,"categorias.html")

@login_required
def categoriadetalhe(request):
    return render(request,"categoriadetalhe.html")

@login_required
def perfil_view(request):
    try:
        user_profile = request.user.profile  # Tenta obter o perfil do usuário logado
    except forms.UserProfile.DoesNotExist:
        user_profile = None

    if request.method == 'POST':
        form = forms.UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            print("Formulário válido!")
            print(f"Data de Nascimento: {form.cleaned_data.get('data_de_nascimento')}")
            form.instance.user = request.user  # Assegura que o perfil está vinculado ao usuário logado
            form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('perfil')  # Substitua 'perfil' pelo nome da sua URL para essa view
        else:
            print("Formulário inválido!")
            # Mensagens de erro detalhadas
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Erro no campo "{field}": {error}')
    else:
        form = forms.UserProfileForm(instance=user_profile)

    return render(request, 'perfil.html', {'form': form})

@login_required
def criar_forum(request):
    if request.method == 'POST':
        form = forms.ForumForm(request.POST)
        if form.is_valid():
            forum = form.save(commit=False)
            forum.usuario = request.user  # Preenche o campo usuário com o usuário logado
            forum.save()
            messages.success(request, 'Fórum criado com sucesso!')
            return redirect('novoforum.html')  # Substitua pela URL de sucesso ou a página desejada
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = forms.ForumForm()


    return render(request, 'novoforum.html', {'form': form})