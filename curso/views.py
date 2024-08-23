from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from . import forms
from .models import Curso, Avaliacao,Modulo,Modulo_usuario,UserProfile,Categorias
from django.db.models import Avg, Count, Sum
from django.core.paginator import Paginator

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
    try:
        # Obter o termo de pesquisa
        busca = request.GET.get('search', '')

        # Filtrar cursos pelo nome, se o termo de busca estiver presente
        if busca:
            todos_cursos = Curso.objects.filter(
                Q(titulo__icontains=busca) | Q(categoria__nome__icontains=busca)
            ).annotate(
                media_avaliacoes=Avg('avaliacao__estrelas'),
                num_avaliacoes=Count('avaliacao')
            ).prefetch_related('avaliacao')
        else:
            todos_cursos = Curso.objects.annotate(
                media_avaliacoes=Avg('avaliacao__estrelas'),
                num_avaliacoes=Count('avaliacao')
            ).prefetch_related('avaliacao')

        # Obter os cursos mais vistos
        cursos_mais_vistos = Curso.objects.annotate(
            media_avaliacoes=Avg('avaliacao__estrelas'),
            num_avaliacoes=Count('avaliacao')
        ).order_by('-visualizacoes')[:5].prefetch_related('avaliacao')

        # Obter os módulos concluídos pelo usuário e filtrar cursos correspondentes
        modulos_concluidos = Modulo_usuario.objects.filter(usuario=request.user, ind_concluido=True).values_list('modulo__curso', flat=True)
        cursos_para_voce = Curso.objects.filter(
            id__in=modulos_concluidos
        ).annotate(
            media_avaliacoes=Avg('avaliacao__estrelas'),
            num_avaliacoes=Count('avaliacao')
        ).prefetch_related('avaliacao')[:5]

        # Formatar dados para o template
        for curso in todos_cursos:
            curso.media_avaliacoes_formatado = f"{curso.media_avaliacoes:.1f}"
            curso.media_avaliacoes_rounded = round(curso.media_avaliacoes)

        for curso in cursos_mais_vistos:
            curso.media_avaliacoes_formatado = f"{curso.media_avaliacoes:.1f}"
            curso.media_avaliacoes_rounded = round(curso.media_avaliacoes)

        for curso in cursos_para_voce:
            curso.media_avaliacoes_formatado = f"{curso.media_avaliacoes:.1f}"
            curso.media_avaliacoes_rounded = round(curso.media_avaliacoes)

        context = {
            'todos_cursos': todos_cursos,
            'cursos_mais_vistos': cursos_mais_vistos,
            'cursos_para_voce': cursos_para_voce,
            'busca': busca,
        }

        return render(request, "cursos.html", context)
    
    except Exception as e:
        # Lidar com erros de consulta ou renderização
        print(f"Erro ao obter cursos: {e}")
        context = {
            'error_message': "Ocorreu um erro ao carregar os cursos."
        }
        return render(request, "cursos.html", context)

@login_required
def meuscursos(request):
    try:
        # Obter o termo de pesquisa
        busca = request.GET.get('search', '')

        # Filtrar cursos iniciados
        modulos_concluidos = Modulo_usuario.objects.filter(usuario=request.user, ind_concluido=False).values_list('modulo__curso', flat=True).distinct()
        cursos_iniciados = Curso.objects.filter(
            id__in=modulos_concluidos,
            titulo__icontains=busca
        ).annotate(
            media_avaliacoes=Avg('avaliacao__estrelas'),
            num_avaliacoes=Count('avaliacao')
        ).prefetch_related('avaliacao')

        # Filtrar cursos recomendados
        modulos_concluidos_recomendados = Modulo_usuario.objects.filter(usuario=request.user, ind_concluido=True).values_list('modulo__curso', flat=True).distinct()
        cursos_para_voce = Curso.objects.filter(
            id__in=modulos_concluidos_recomendados,
            titulo__icontains=busca
        ).annotate(
            media_avaliacoes=Avg('avaliacao__estrelas'),
            num_avaliacoes=Count('avaliacao')
        ).prefetch_related('avaliacao')[:5]

        # Formatar dados e calcular avaliação com estrela meia
        for curso in cursos_iniciados:
            curso.media_avaliacoes_formatado = f"{curso.media_avaliacoes:.1f}" if curso.media_avaliacoes is not None else "0.0"
            curso.show_half_star = (float(curso.media_avaliacoes_formatado) % 1) >= 0.5

        for curso in cursos_para_voce:
            curso.media_avaliacoes_formatado = f"{curso.media_avaliacoes:.1f}" if curso.media_avaliacoes is not None else "0.0"
            curso.show_half_star = (float(curso.media_avaliacoes_formatado) % 1) >= 0.5

        context = {
            'cursos_iniciados': cursos_iniciados,
            'cursos_para_voce': cursos_para_voce,
            'busca': busca,
        }

        return render(request, "meuscursos.html", context)
    
    except Exception as e:
        # Lidar com erros de consulta ou renderização
        print(f"Erro ao obter cursos: {e}")
        context = {
            'error_message': "Ocorreu um erro ao carregar os cursos.",
            'busca': busca,
        }
        return render(request, "meuscursos.html", context)


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
    query = request.GET.get('q', '')  # Obtém o valor da consulta de pesquisa

    if query:
        professores = UserProfile.objects.filter(user__username__icontains=query, tipo=UserProfile.PROFESSOR)
    else:
        professores = UserProfile.objects.filter(tipo=UserProfile.PROFESSOR)
    
    # Paginação
    paginator = Paginator(professores, 6)  # Mostra 6 professores por página
    page_number = request.GET.get('page')  # Obtém o número da página da requisição
    page_obj = paginator.get_page(page_number)  # Obtém a página atual

    context = {
        'page_obj': page_obj,
        'query': query
    }
    
    return render(request, "professores.html", context)

@login_required
def redecredenciada(request):
    return render(request,"redecredenciada.html")

@login_required
def categorias(request):
    categorias = Categorias.objects.annotate(num_cursos=Count('curso'))
    total_cursos = categorias.aggregate(total=Sum('num_cursos'))['total'] or 0
    return render(request, "categorias.html", {'categorias': categorias, 'total_cursos': total_cursos})

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