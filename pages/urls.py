from django.urls import path
from . import views

urlpatterns = [
    path('', views.vue_accueil, name='accueil'),
    path('a-propos/', views.vue_a_propos, name='a_propos'),
    path('createur/', views.vue_createur, name='createur'),
    path('bibliographie/', views.vue_bibliographie, name='bibliographie'),
]
