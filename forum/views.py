from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TopicoForum, RespostaForum
from curso.models import Curso
from .forms import FormularioTopico, FormularioResposta

@login_required
def lista_forum(request):
    query = request.GET.get('q')  # Captura o termo de busca do input
    
    if query:
        topicos = TopicoForum.objects.filter(titulo__icontains=query).order_by('-data_criacao')
    else:
        topicos = TopicoForum.objects.all().order_by('-data_criacao')
    
    return render(request, 'lista_forum.html', {'topicos': topicos, 'query': query})

@login_required
def criar_topico(request):
    if request.method == 'POST':
        formulario = FormularioTopico(request.POST, request.FILES)  # Adicione request.FILES aqui
        if formulario.is_valid():
            topico = formulario.save(commit=False)
            topico.usuario = request.user
            topico.save()
            messages.success(request, 'Fórum criado com sucesso!')
            return redirect('detalhe_forum', pk=topico.pk)
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        formulario = FormularioTopico()
    return render(request, 'criar_topico.html', {'formulario': formulario})

@login_required
def detalhe_forum(request, pk):
    topico = get_object_or_404(TopicoForum, pk=pk)
    respostas = topico.respostas.all().order_by('data_criacao')
    
    if request.method == 'POST':
        formulario = FormularioResposta(request.POST)
        if formulario.is_valid():
            resposta = formulario.save(commit=False)
            resposta.topico = topico
            resposta.usuario = request.user
            resposta.save()
            messages.success(request, 'Sua resposta foi enviada com sucesso!')
            return redirect('detalhe_forum', pk=pk)
    else:
        formulario = FormularioResposta()
    
    return render(request, 'detalhe_forum.html', {'topico': topico, 'respostas': respostas, 'formulario': formulario})