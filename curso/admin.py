from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    Curso, UserProfile, Modulo_usuario, Modulo, Categorias, Questionario,
    Aula, Chat, Badge, Forum, Avaliacao, Pergunta, Certificado,
    Alternativas, LaudosMedicos, Agendamento
)
from .forms import UserProfileForm, AgendamentoForm





# Filtro personalizado
class UserCreationDateListFilter(admin.SimpleListFilter):
    title = _('user creation date')
    parameter_name = 'user_creation_date'

    def lookups(self, request, model_admin):
        users = set([profile.user for profile in UserProfile.objects.all()])
        return [(user.id, user.date_joined.date()) for user in users]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(user__date_joined__date=self.value())
        return queryset

class UserProfileAdmin(admin.ModelAdmin):
    form = UserProfileForm
    list_display = ['user', 'foto', 'data_de_nascimento', 'facebook', 'linkedin', 'google_plus', 'descricao', 'web_site', 'tipo']
    list_filter = ['tipo', UserCreationDateListFilter]  # Adiciona o filtro personalizado
    search_fields = ['user__username', 'user__email', 'tipo']
class AgendamentoAdmin(admin.ModelAdmin):
    form = AgendamentoForm

admin.site.register(Agendamento, AgendamentoAdmin)
admin.site.register(Curso)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Modulo_usuario)
admin.site.register(Modulo)
admin.site.register(Categorias)
admin.site.register(Questionario)
admin.site.register(Aula)
admin.site.register(Chat)
admin.site.register(Badge)
admin.site.register(Forum)
admin.site.register(Avaliacao)
admin.site.register(Pergunta)
admin.site.register(Certificado)
admin.site.register(Alternativas)
admin.site.register(LaudosMedicos)
