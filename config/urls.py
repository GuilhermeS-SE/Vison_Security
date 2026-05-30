from django.contrib import admin
from django.urls import path, include

from scanner_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing, name='landing'),           # Tela de apresentação
    path('scanner_app/', views.home, name='home'),         # Tela do formulário (VISION)
    path('scanner_app/run/', views.run_scan, name='scan'), # Processamento e Relatório
]