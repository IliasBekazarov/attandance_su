
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.conf.urls.i18n import i18n_patterns
from django.http import JsonResponse

def chrome_devtools_json(request):
    """Chrome DevTools үчүн жооп"""
    return JsonResponse({}, status=200)

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # Language switching
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),
    path('.well-known/appspecific/com.chrome.devtools.json', chrome_devtools_json, name='chrome_devtools'),
]

# Add i18n patterns for multilingual URLs
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('api/v1/', include('core.api_urls')),  # API endpoints
)

# Static жана media файлдар үчүн URL'дер (development режиминде)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) if hasattr(settings, 'MEDIA_URL') else []
