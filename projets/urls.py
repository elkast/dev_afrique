from django.urls import path
from . import views

urlpatterns = [
    path('', views.vue_liste_projets, name='liste_projets'),
    path('soumettre/', views.vue_soumettre_projet, name='soumettre_projet'),
    path('<slug:slug>/', views.vue_detail_projet, name='detail_projet'),
    path('<slug:slug>/liker/', views.vue_liker_projet, name='liker_projet'),
    path('<slug:slug>/commenter/', views.vue_commenter_projet, name='commenter_projet'),
]
