from django.urls import path
from . import views

urlpatterns = [
    path('', views.vue_tableau_dmz, name='dmz_tableau'),
    path('journal/', views.vue_journal_securite, name='dmz_journal'),
    path('ips/', views.vue_ips_bloquees, name='dmz_ips_bloquees'),
    path('ips/bloquer/', views.vue_bloquer_ip, name='dmz_bloquer_ip'),
    path('ips/<int:pk>/debloquer/', views.vue_debloquer_ip, name='dmz_debloquer_ip'),
    path('tentatives/', views.vue_tentatives_connexion, name='dmz_tentatives'),
    path('tentatives-admin/', views.vue_tentatives_admin, name='dmz_tentatives_admin'),
]
