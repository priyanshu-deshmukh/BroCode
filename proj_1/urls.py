
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth_0/", include('auth_0.urls')),
    path("", include('home.urls')),
    path("llm/", include('llm.urls')),
]
