from django.urls import path
from . import views

urlpatterns = [
    path('', views.vue_glossaire, name='glossaire'),
    path('<slug:slug>/', views.vue_detail_terme, name='glossaire_detail'),
]
