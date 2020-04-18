from .auth import register_page, login_page, logout_page
from .profile import profile_page, profile_edit_page, delete_avatar, change_password
from .search import search_page
from .track import music_track_page, popular_tracks
from .project import new_project, project_home, projects_list, editor
from .instrument import instruments, new_instrument

from .util import get_base_context, render


def index(request):
    '''
    Главная страница

    :param request: запрос клиента
    :return: главная страница
    :rtype: HttpResponse
    '''

    return render(request, 'index.html', get_base_context(request))