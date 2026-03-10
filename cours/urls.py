from django.urls import path
from . import views

urlpatterns = [
    path('', views.vue_liste_cours, name='liste_cours'),
    path('parcours/', views.vue_liste_parcours, name='liste_parcours'),
    path('parcours/<slug:slug>/', views.vue_detail_parcours, name='detail_parcours'),
    path('<slug:slug>/', views.vue_detail_cours, name='detail_cours'),
    path('<slug:cours_slug>/lecon/<slug:lecon_slug>/', views.vue_lecon, name='lecon'),
    path('<slug:cours_slug>/lecon/<slug:lecon_slug>/terminer/', views.vue_marquer_terminee, name='marquer_terminee'),
]
