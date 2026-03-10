from django.urls import path
from . import views

urlpatterns = [
    path('', views.vue_tableau_de_bord, name='tableau_de_bord'),
    # Parcours
    path('parcours/', views.vue_liste_parcours_admin, name='admin_liste_parcours'),
    path('parcours/creer/', views.vue_creer_parcours, name='admin_creer_parcours'),
    path('parcours/<int:pk>/modifier/', views.vue_modifier_parcours, name='admin_modifier_parcours'),
    path('parcours/<int:pk>/supprimer/', views.vue_supprimer_parcours, name='admin_supprimer_parcours'),
    # Cours
    path('cours/', views.vue_liste_cours_admin, name='admin_liste_cours'),
    path('cours/creer/', views.vue_creer_cours, name='admin_creer_cours'),
    path('cours/<int:pk>/modifier/', views.vue_modifier_cours, name='admin_modifier_cours'),
    path('cours/<int:pk>/supprimer/', views.vue_supprimer_cours, name='admin_supprimer_cours'),
    # Leçons
    path('lecons/', views.vue_liste_lecons_admin, name='admin_liste_lecons'),
    path('lecons/creer/', views.vue_creer_lecon, name='admin_creer_lecon'),
    path('lecons/<int:pk>/modifier/', views.vue_modifier_lecon, name='admin_modifier_lecon'),
    path('lecons/<int:pk>/supprimer/', views.vue_supprimer_lecon, name='admin_supprimer_lecon'),
    # Projets
    path('projets/', views.vue_liste_projets_admin, name='admin_liste_projets'),
    path('projets/<int:pk>/moderer/', views.vue_moderer_projet, name='admin_moderer_projet'),
    # Utilisateurs
    path('utilisateurs/', views.vue_liste_utilisateurs_admin, name='admin_liste_utilisateurs'),
    path('utilisateurs/<int:pk>/role/', views.vue_modifier_role, name='admin_modifier_role'),
    # Signalements
    path('signalements/', views.vue_liste_signalements, name='admin_liste_signalements'),
    path('signalements/<int:pk>/traiter/', views.vue_traiter_signalement, name='admin_traiter_signalement'),
    # Glossaire
    path('glossaire/', views.vue_liste_glossaire_admin, name='admin_liste_glossaire'),
    path('glossaire/creer/', views.vue_creer_terme, name='admin_creer_terme'),
    path('glossaire/<int:pk>/modifier/', views.vue_modifier_terme, name='admin_modifier_terme'),
    path('glossaire/<int:pk>/supprimer/', views.vue_supprimer_terme, name='admin_supprimer_terme'),
]
