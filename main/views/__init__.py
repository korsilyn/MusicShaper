'''
Главный модуль папки views
'''

from django.shortcuts import render
from django.contrib.auth.models import User

from .auth import register_page, login_page, logout_page
from .profile import profile_page, profile_edit_page, delete_avatar,\
    change_password, subscribe, unsubscribe, subscriptions_page
from .search import search_page
from .track import track_view, popular_tracks, upload_track, delete_track, manage_track,\
    listen_track
from .claim_track import claim_track
from .project import new_project, project_home, manage_project, delete_project, projects_list,\
    project_timeline, save_timeline
from .instrument import instruments, new_instrument, edit_instrument,\
    manage_instrument, delete_instrument, get_instrument_ajax
from .pattern import patterns_list, new_pattern, pattern_editor, manage_pattern, delete_pattern,\
    save_pattern
from .admin import admin_home, create_test_track, claimed_tracks

from .util import get_base_context


def index(request):
    '''
    Главная страница

    :param request: запрос клиента
    :return: главная страница
    :rtype: HttpResponse
    '''

    return render(request, 'index.html', get_base_context(request))
