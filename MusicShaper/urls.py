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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from main import views

urlpatterns = [
    path('', views.index, name='index'),

    path('admin/', include([
        path('', views.admin_home, name='admin_home'),
        path('django/', admin.site.urls),
        path('create_test_track', views.create_test_track, name='create_test_track'),
    ])),

    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),

    path('profile/', include([
        path('', views.profile_page, {'username': None}, name='profile'),
        path('edit/', views.profile_edit_page, name='profile_edit'),
        path('delete_avatar/', views.delete_avatar, name='delete_avatar'),
        path('change_password/', views.change_password, name='change_password'),
    ])),
    path('profile/<str:username>/', include([
        path('', views.profile_page, name='profile'),
        path('sub', views.subscribe, name='subscribe'),
        path('unsub', views.unsubscribe, name='unsubscribe'),
    ])),

    path('project/', include([
        path('list/', views.projects_list, name='projects'),
        path('new/', views.new_project, name='new_project')
    ])),
    path('project/<int:proj_id>/', include([
        path('', views.project_home, name='project_home'),
        path('manage/', views.manage_project, name='manage_project'),
        path('delete/', views.delete_project, name='delete_project'),
        path('instrument/', include([
            path('list/', views.instruments, name='instruments'),
            path('new/', views.new_instrument, name='new_instrument'),
        ])),
        path('instrument/<int:instr_id>/', include([
            path('', views.edit_instrument, name='edit_instrument'),
            path('manage/', views.manage_instrument, name='manage_instrument'),
            path('delete/', views.delete_instrument, name='delete_instrument'),
        ])),
    ])),

    path('track/popular/', views.popular_tracks, name='popular_tracks'),
    path('track/<int:track_id>/', include([
        path('', views.track_view, name='track'),
    ])),

    path('search/', views.search_page, name='search'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
