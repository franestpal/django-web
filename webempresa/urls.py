from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Paths del core
    path('', include('core.urls')),
    # Paths de services
    path('services/', include('services.urls')),
    # Paths de recetas
    path('blog/', include('blog.urls')),
    # Paths de pages
    path('page/', include('pages.urls')),
    # Paths de pages
    path('contact/', include('contact.urls')),
    # Paths del admin
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
        # Paths de profiles
    path('profile/', include('registration.urls')),
    path('store/', include('store.urls')),


    
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)