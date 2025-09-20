"""
URL configuration for proj_bd project.

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
from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # define as rotas de URL da nossa aplicacao
    path('', views.home, name='home'),
    path('dados_gerais/', views.dados_gerais, name='dados_gerais'),
    path('campi_por_uf/', views.campi_por_uf, name='campi_por_uf'),
    path('curso_por_area/', views.curso_por_area, name='curso_por_area'),
    path('ranking_dos_cursos_por_uf/', views.ranking_dos_cursos_por_uf, name='ranking_dos_cursos_por_uf'),
    path('ranking_por_municipio/', views.ranking_por_municipio, name='ranking_por_municipio'),
] 
