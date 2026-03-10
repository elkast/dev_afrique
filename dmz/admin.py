from django.contrib import admin
from .models import TentativeConnexion, IPBloquee, JournalSecurite, TentativeAdmin


@admin.register(TentativeConnexion)
class TentativeConnexionAdmin(admin.ModelAdmin):
    list_display = ['adresse_ip', 'nom_utilisateur', 'reussie', 'date']
    list_filter = ['reussie', 'date']
    search_fields = ['adresse_ip', 'nom_utilisateur']
    readonly_fields = ['adresse_ip', 'nom_utilisateur', 'user_agent', 'reussie', 'date']


@admin.register(IPBloquee)
class IPBloqueeAdmin(admin.ModelAdmin):
    list_display = ['adresse_ip', 'raison', 'est_actif', 'nombre_tentatives', 'date_blocage']
    list_filter = ['raison', 'est_actif']
    search_fields = ['adresse_ip']


@admin.register(JournalSecurite)
class JournalSecuriteAdmin(admin.ModelAdmin):
    list_display = ['type_evenement', 'niveau', 'adresse_ip', 'description', 'date']
    list_filter = ['type_evenement', 'niveau', 'date']
    search_fields = ['adresse_ip', 'description']


@admin.register(TentativeAdmin)
class TentativeAdminAdmin(admin.ModelAdmin):
    list_display = ['adresse_ip', 'nom_utilisateur', 'reussie', 'date']
    list_filter = ['reussie', 'date']
