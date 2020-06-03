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
    path('asds1231okasd2i9dsja', views.superuser, name='adminnnnn'),

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
        path('subscriptions/', views.subscriptions_page, name='subscriptions'),
        path('<str:username>/', include([
            path('', views.profile_page, name='profile'),
            path('sub', views.subscribe, name='subscribe'),
            path('unsub', views.unsubscribe, name='unsubscribe'),
        ])),
    ])),

    path('projects/', include([
        path('', views.projects_list, name='projects'),
        path('new/', views.new_project, name='new_project'),
        path('<int:proj_id>/', include([
            path('', views.project_home, name='project_home'),
            path('manage/', views.manage_project, name='manage_project'),
            path('delete/', views.delete_project, name='delete_project'),

            path('instruments/', include([
                path('', views.instruments, name='instruments'),
                path('new/', views.new_instrument, name='new_instrument'),
                path('get/', views.get_instrument_ajax, name='get_instrument'),
                path('<int:instr_id>/', include([
                    path('', views.edit_instrument, name='edit_instrument'),
                    path('manage/', views.manage_instrument, name='manage_instrument'),
                    path('delete/', views.delete_instrument, name='delete_instrument'),
                ])),
            ])),

            path('patterns/', include([
                path('', views.patterns_list, name='patterns'),
                path('new/', views.new_pattern, name='new_pattern'),
                path('<int:pat_id>/', include([
                    path('', views.pattern_editor, name='pattern_editor'),
                    path('manage/', views.manage_pattern, name='manage_pattern'),
                    path('delete/', views.delete_pattern, name='delete_pattern'),
                    path('save/', views.save_pattern, name='save_pattern'),
                ])),
            ])),

            path('timeline/', include([
                path('', views.project_timeline, name='timeline'),
                path('save/', views.save_timeline, name='save_timeline'),
            ])),
        ])),
    ])),

    path('tracks/', include([
        path('', views.popular_tracks, name='popular_tracks'),
        path('<int:track_id>/', include([
            path('', views.track_view, name='track'),
        ])),
    ])),

    path('search/', views.search_page, name='search'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
