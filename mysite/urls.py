from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Pythonfun.urls', namespace='Pythonfun')),
    # 添加Django默认认证URL的重定向
    path('accounts/login/', RedirectView.as_view(url='/login/', permanent=True)),
]
