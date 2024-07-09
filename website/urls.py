"""
URL configuration for website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from typing import Sequence

from django.contrib import admin
from django.urls import path, include, URLResolver
from django.conf import settings

from debug_toolbar.settings import CONFIG_DEFAULTS

# Define the urlpatterns list to store the URL patterns
urlpatterns: Sequence[URLResolver] = [
    path("blog/", include("blog.urls")),  # Include the URLs from the 'blog' app
    path('admin/', admin.site.urls),  # Include the admin URLs
]

# Add debug toolbar URLs if the application is not being tested
if not CONFIG_DEFAULTS['IS_RUNNING_TESTS']:
    urlpatterns = [
        *urlpatterns,
        path("__debug__/", include("debug_toolbar.urls")),
    ]

# Add static URLs for media files if DEBUG mode is enabled
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns = [
        *urlpatterns,
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    ]
    
