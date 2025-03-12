"""
URL configuration for proiect project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

from django.conf import settings # it accesses settings.py from upper
from django.conf.urls.static import static

from core.views import index, category_detail, category_list
urlpatterns = [
    path('admin/', admin.site.urls),
    # path("", index)
    path("", include("core.urls")),
    path("user/", include("userauths.urls")),    
    path('', include('core.urls')),
    path('', index, name='index'),
    path('categories/', category_list, name='category_list'),  # Verifică acest nume
path('category/<str:category_id>/', category_detail, name='category_detail'),
]

# all thr static files are stored in teh static directory in root directory

if settings.DEBUG:     
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
