
from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.generic import DetailView
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


from . import forms
from .models import Curso, Avaliacao, Modulo, Modulo_usuario, UserProfile, Categorias, Aula,Progresso,Alternativas,Questionario,Pergunta
from django.db.models import Avg, Count, Sum, Q
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
    cursos_mais_vistos = Curso.objects.annotate(
        media_avaliacoes=Avg('avaliacao__estrelas'),
        num_avaliacoes=Count('avaliacao')
    ).order_by('-visualizacoes').prefetch_related('avaliacao')
    
    cursos_recem_adicionados = Curso.objects.annotate(
        media_avaliacoes=Avg('avaliacao__estrelas'),
        num_avaliacoes=Count('avaliacao')
    ).order_by('-data_criacao').prefetch_related('avaliacao')

    context = {
        'cursos_mais_vistos': cursos_mais_vistos,
        'cursos_recem_adicionados': cursos_recem_adicionados,
    }

    return render(request, "homepage.html", context)



@login_required
def cursos(request):
    try:
        busca = request.GET.get('search', '')
        print(f"Termo de busca: '{busca}'")

        if busca:
            todos_cursos = Curso.objects.filter(
                Q(titulo__icontains=busca) | 
                Q(descricao__icontains=busca)
            ).annotate(
                media_avaliacoes=Avg('avaliacao__estrelas'),
                num_avaliacoes=Count('avaliacao')
            ).prefetch_related('avaliacao')
        else:
            todos_cursos = Curso.objects.annotate(
                media_avaliacoes=Avg('avaliacao__estrelas'),
                num_avaliacoes=Count('avaliacao')
            ).prefetch_related('avaliacao')

        print(f"Número de todos os cursos: {todos_cursos.count()}")

        # Formatar dados para o template
        for curso in todos_cursos:
            if curso.media_avaliacoes is not None:
                curso.media_avaliacoes_formatado = f"{curso.media_avaliacoes:.1f}"
                curso.media_avaliacoes_rounded = round(curso.media_avaliacoes)
            else:
                curso.media_avaliacoes_formatado = "0.0"
                curso.media_avaliacoes_rounded = 0

        context = {
            'todos_cursos': todos_cursos,
            'busca': busca  # Para manter o valor de busca no formulário
        }

        return render(request, "cursos.html", context)

    except Exception as e:
        print(f"Erro ao buscar cursos: {e}")
        return render(request, "cursos.html", {"error": "Erro ao carregar cursos."})

@login_required
def meuscursos(request):
    try:
        # Obter o termo de pesquisa
        busca = request.GET.get('search', '')

        # Filtrar cursos iniciados
        modulos_concluidos = Modulo_usuario.objects.filter(usuario=request.user, ind_concluido=False).values_list(
            'modulo__curso', flat=True).distinct()
        cursos_iniciados = Curso.objects.filter(
            id__in=modulos_concluidos,
            titulo__icontains=busca
        ).annotate(
            media_avaliacoes=Avg('avaliacao__estrelas'),
            num_avaliacoes=Count('avaliacao')
        ).prefetch_related('avaliacao')

        # Filtrar cursos recomendados
        modulos_concluidos_recomendados = Modulo_usuario.objects.filter(usuario=request.user,
                                                                        ind_concluido=True).values_list('modulo__curso',
                                                                                                        flat=True).distinct()
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
def cursodetalhe(request, pk):
    try:
        # Busca o curso pelo ID (pk)
        curso = Curso.objects.get(pk=pk)
        avaliacoes = Avaliacao.objects.filter(curso=curso).order_by('-data_criacao')
        
        # Usando 'modulos' instead of 'modulo_set' to access the módulos do curso
        modulos = curso.modulos.all().order_by('ordem').prefetch_related('aulas')
        
        # Obter a primeira aula do primeiro módulo
        primeira_aula = None
        if modulos.exists():
            primeira_aula = modulos.first().aulas.first()
        
        # Cálculo de média das avaliações
        media_avaliacoes = Avaliacao.objects.filter(curso=curso).aggregate(Avg('estrelas'))['estrelas__avg']
        estrelas_inteiras = int(media_avaliacoes) if media_avaliacoes else 0
        meia_estrela = (media_avaliacoes - estrelas_inteiras) >= 0.5 if media_avaliacoes else False
        estrelas_vazias = 5 - estrelas_inteiras - (1 if meia_estrela else 0)
        
        # Obter as aulas já concluídas pelo usuário
        progresso_usuario = Progresso.objects.filter(usuario=request.user, aula__modulo__curso=curso)
        aulas_concluidas = progresso_usuario.filter(completado=True).values_list('aula_id', flat=True)
        
        # Contar total de aulas do curso
        total_aulas = curso.modulos.annotate(total_aulas=Count('aulas')).aggregate(total=Sum('total_aulas'))['total'] or 0
        
        # Contar aulas concluídas pelo usuário
        total_aulas_concluidas = progresso_usuario.filter(completado=True).count()
        
        # Calcular porcentagem de conclusão
        porcentagem_conclusao = (total_aulas_concluidas / total_aulas * 100) if total_aulas > 0 else 0
        
        # Obter questionários e perguntas para cada módulo
        for modulo in modulos:
            modulo.questionario = Questionario.objects.filter(modulo=modulo).first()
            if modulo.questionario:
                modulo.perguntas = Pergunta.objects.filter(questionario=modulo.questionario).prefetch_related('alternativas_set')

        context = {
            'curso': curso,
            'modulos': modulos,
            'avaliacoes': avaliacoes,
            'media_avaliacoes': media_avaliacoes,
            'estrelas_inteiras': range(estrelas_inteiras),
            'estrelas_vazias': range(estrelas_vazias),
            'meia_estrela': meia_estrela,
            'primeira_aula': primeira_aula,
            'aulas_concluidas': aulas_concluidas,
            'porcentagem_conclusao': porcentagem_conclusao,
        }
        
        return render(request, "cursodetalhe.html", context)
    
    except Curso.DoesNotExist:
        messages.error(request, 'Curso não encontrado.')
        return redirect('cursos')


@login_required
def foruns(request):
    return render(request, "foruns.html")


@login_required
def forumdetalhe(request):
    return render(request, "forumdetalhe.html")


@login_required
def documentos(request):
    return render(request, "documentos.html")


@login_required
def perfil(request):
    return render(request, "perfil.html")


@login_required
def professordetalhe(request):
    return render(request, "professordetalhe.html")


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
    return render(request, "redecredenciada.html")


@login_required
def categorias(request):
    categorias = Categorias.objects.annotate(num_cursos=Count('curso'))
    total_cursos = categorias.aggregate(total=Sum('num_cursos'))['total'] or 0
    return render(request, "categorias.html", {'categorias': categorias, 'total_cursos': total_cursos})


@login_required
def categoriadetalhe(request, id):
    busca = request.GET.get('search', '')
    
    # Obtém a categoria pelo id
    categoria = Categorias.objects.get(pk=id)

    # Filtra cursos por categoria e, opcionalmente, por busca
    if busca:
        todos_cursos = Curso.objects.filter(
            categoria=categoria,
            titulo__icontains=busca
        ).annotate(
            media_avaliacoes=Avg('avaliacao__estrelas'),
            num_avaliacoes=Count('avaliacao')
        ).prefetch_related('avaliacao')
    else:
        todos_cursos = Curso.objects.filter(categoria=categoria).annotate(
            media_avaliacoes=Avg('avaliacao__estrelas'),
            num_avaliacoes=Count('avaliacao')
        ).prefetch_related('avaliacao')
    
    context = {
        'todos_cursos': todos_cursos,
        'categoria': categoria  # Passa a categoria para o template
    }
    return render(request, "categoriadetalhe.html", context)


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


def conheca(request):
    return render(request, "conheca.html")

def fale_conosco(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        assunto = request.POST.get('assunto')
        mensagem = request.POST.get('mensagem')
        termos = request.POST.get('termos')
        recaptcha_response = request.POST.get('g-recaptcha-response')
        
        # Verifica o reCAPTCHA
        recaptcha_url = 'https://www.google.com/recaptcha/api/siteverify'
        recaptcha_data = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        # recaptcha_result = requests.post(recaptcha_url, data=recaptcha_data)
        # result_json = recaptcha_result.json()

        # Verifica se o reCAPTCHA foi bem-sucedido
        if True:
            # Enviar email
            send_mail(
                f"{assunto} - de {nome} {sobrenome}",
                mensagem,
                email,  # De quem é o email
                ['seu_email@exemplo.com'],  # Para onde o email vai
                fail_silently=False,
            )
            messages.success(request, 'Sua mensagem foi enviada com sucesso.')
            return redirect('faleconosco')  # Redireciona de volta para a página
        else:
            messages.error(request, 'Erro no reCAPTCHA. Por favor, tente novamente.')
    
    return render(request, 'faleconosco.html')

@csrf_exempt
def salvar_progresso(request, aula_id):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            aula = Aula.objects.get(id=aula_id)
            progresso, created = Progresso.objects.get_or_create(usuario=request.user, aula=aula)

            # Marcar como completado
            progresso.completado = True
            progresso.save()

            return JsonResponse({'status': 'ok', 'message': 'Progresso salvo com sucesso!'})
        except Aula.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Aula não encontrada'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Requisição inválida'})
    
    
    
def politica_privacidade(request):
    return render(request, "politicaPrivacidade.html")

@login_required
@require_POST
def processa_quiz(request):
    respostas = {key: value for key, value in request.POST.items() if key.startswith('pergunta_')}
    
    pontuacao = 0
    total_perguntas = len(respostas)
    
    for pergunta_id, alternativa_id in respostas.items():
        pergunta_id = pergunta_id.split('_')[1]  # Extrair o ID da pergunta
        try:
            alternativa = Alternativas.objects.get(id=alternativa_id)
            if alternativa.resposta_correta:
                pontuacao += 1
        except Alternativas.DoesNotExist:
            # Opcional: Logar ou tratar caso a alternativa não exista
            continue  # Pular para a próxima pergunta
    
    porcentagem_acertos = (pontuacao / total_perguntas) * 100 if total_perguntas > 0 else 0
    passou = porcentagem_acertos >= 70
    
    # Lógica para atualizar o progresso do usuário (opcional)
    
    return JsonResponse({
        'message': f'Você acertou {pontuacao} de {total_perguntas} perguntas.',
        'porcentagem': porcentagem_acertos,
        'passou': passou
    })