from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import TopicoForum, RespostaForum
from curso.models import Curso
from .forms import FormularioTopico, FormularioResposta

def lista_forum(request):
    topicos = TopicoForum.objects.all().order_by('-data_criacao')
    return render(request, 'lista_forum.html', {'topicos': topicos})

@login_required
def criar_topico(request):
    if request.method == 'POST':
        formulario = FormularioTopico(request.POST)
        if formulario.is_valid():
            topico = formulario.save(commit=False)
            topico.usuario = request.user
            topico.save()
            return redirect('detalhe_forum', pk=topico.pk)
    else:
        formulario = FormularioTopico()
    return render(request, 'criar_topico.html', {'formulario': formulario})

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
            return redirect('detalhe_forum', pk=pk)
    else:
        formulario = FormularioResposta()
    return render(request, 'detalhe_forum.html', {'topico': topico, 'respostas': respostas, 'formulario': formulario})