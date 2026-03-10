from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('pages.urls')),
    path('cours/', include('cours.urls')),
    path('utilisateurs/', include('utilisateurs.urls')),
    path('projets/', include('projets.urls')),
    path('forum/', include('forum.urls')),
    path('glossaire/', include('glossaire.urls')),
    path('administration/', include('administration.urls')),
    path('administration/dmz/', include('dmz.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ─── HTTP Error Handlers ─────────────────────────────────────
handler400 = 'pages.views.vue_erreur_400'
handler403 = 'pages.views.vue_erreur_403'
handler404 = 'pages.views.vue_erreur_404'
handler500 = 'pages.views.vue_erreur_500'
