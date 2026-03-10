from django.urls import path
from . import views

urlpatterns = [
    path('', views.vue_liste_sujets, name='forum'),
    path('nouveau/', views.vue_nouveau_sujet, name='forum_nouveau'),
    path('<slug:slug>/', views.vue_detail_sujet, name='forum_detail'),
    path('<slug:slug>/repondre/', views.vue_repondre, name='forum_repondre'),
    path('<slug:slug>/resoudre/<int:reponse_id>/', views.vue_marquer_solution, name='forum_solution'),
]
