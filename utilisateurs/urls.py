from django.urls import path
from . import views

urlpatterns = [
    path('inscription/', views.vue_inscription, name='inscription'),
    path('connexion/', views.vue_connexion, name='connexion'),
    path('deconnexion/', views.vue_deconnexion, name='deconnexion'),
    path('profil/', views.vue_profil, name='profil'),
    path('<str:username>/', views.vue_profil_public, name='profil_public'),
]
