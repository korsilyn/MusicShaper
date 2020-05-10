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
from django.conf import settings
from django.conf.urls.static import static
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('popular_tracks/', views.popular_tracks, name='popular_tracks'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('logout/', views.logout_page, name='logout'),
    path('profile/', views.profile_page, name='profile'),
    path('profile/edit', views.profile_edit_page, name='profile_edit'),
    path('profile/delete_avatar', views.delete_avatar, name='delete_avatar'),
    path('profile/change_password', views.change_password, name='change_password'),
    path('profile/sub/<int:pk>', views.subscribe, name='subscribe'),
    path('profile/unsub/<int:pk>', views.unsubscribe, name='unsubscribe'),
    path('projects', views.projects_list, name='projects'),
    path('project/new', views.new_project, name='new_project'),
    path('project/<int:proj_id>/home', views.project_home, name='project_home'),
    path('project/<int:proj_id>/manage',
         views.manage_project, name='manage_project'),
    path('project/<int:proj_id>/delete',
         views.delete_project, name='delete_project'),
    path('project/<int:proj_id>/instruments',
         views.instruments, name='instruments'),
    path('project/<int:proj_id>/instrument/new',
         views.new_instrument, name='new_instrument'),
    path('project/<int:proj_id>/instrument/<int:instr_id>',
         views.edit_instrument, name='edit_instrument'),
    path('project/<int:proj_id>/instrument/<int:instr_id>/manage',
         views.manage_instrument, name='manage_instrument'),
    path('project/<int:proj_id>/instrument/<int:instr_id>/delete',
         views.delete_instrument, name='delete_instrument'),
    path('track/<int:track_id>', views.track_view, name='track'),
    path('search/', views.search_page, name='search'),
    path('admin_home/create_test_track',
         views.create_test_track, name='create_test_track'),
    path('admin_home/', views.admin_home, name='admin_home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
