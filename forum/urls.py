from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_forum, name='lista_forum'),
    path('criar/', views.criar_topico, name='criar_topico'),
    path('<int:pk>/', views.detalhe_forum, name='detalhe_forum'),
]