"""MusicShaper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from main import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('editor/', views.editor, name='editor'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('logout/', views.logout_page, name='logout'),
    path('profile/', views.profile_page, name='profile'),
    path('projects', views.projects_list, name='projects'),
    path('project/new', views.new_project, name='new_project'),
    path('project/<int:id>/home', views.project_home, name='project_home'),
    path('project/<int:id>/instruments',
         views.project_instruments_list, name='project_instruments'),
    path('project/<int:id>/instrument/new',
         views.project_new_instrument, name='project_new_instrument'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)