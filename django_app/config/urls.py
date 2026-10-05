import os
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import include, path


def service_worker(request):
    """Serve service worker script with Service-Worker-Allowed header at root scope."""
    sw_path = os.path.join(settings.BASE_DIR, 'static', 'sw.js')
    if os.path.exists(sw_path):
        with open(sw_path, 'r', encoding='utf-8') as f:
            content = f.read()
        response = HttpResponse(content, content_type='application/javascript')
        response['Service-Worker-Allowed'] = '/'
        return response
    return HttpResponse("// sw.js not found", content_type='application/javascript', status=404)


def admin_dashboard_redirect(request):
    return redirect('core:dashboard')


urlpatterns = [
    path('sw.js', service_worker, name='service_worker'),
    path('django-admin/', admin.site.urls), path('', include('apps.core.urls')),
    path('student/', include('apps.accounts.student_urls')),
    path('blogs/', include('apps.blog.urls')), path('events/', include('apps.events.urls')),
    path('news/', include('apps.news.urls')),
    path('faculty/', include('apps.faculty.urls')), path('contact/', include('apps.contact.urls')),
    path('admin/', admin_dashboard_redirect, name='admin_root'),
    path('admin/', include('apps.accounts.urls')), path('admin/', include('apps.core.admin_urls')),
    path('admin/', include('apps.blog.admin_urls')),
    path('admin/', include('apps.events.admin_urls')), path('admin/', include('apps.faculty.admin_urls')),
    path('admin/', include('apps.news.admin_urls')),
    path('admin/', include('apps.gallery.urls')), path('admin/', include('apps.contact.admin_urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
# Render does not provide a separate media server. Serve uploaded files through
# Django so every FileField URL works without a paid persistent disk.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
