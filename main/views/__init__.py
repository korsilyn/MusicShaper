from .auth import register_page, login_page, logout_page
from .profile import profile_page, profile_edit_page, delete_avatar, change_password
from .search import search_page
from .track import track_view, popular_tracks
from .project import new_project, project_home, manage_project, delete_project, projects_list
from .instrument import instruments, new_instrument, edit_instrument, manage_instrument, delete_instrument

from .util import get_base_context, render


def index(request):
    '''
    Главная страница

    :param request: запрос клиента
    :return: главная страница
    :rtype: HttpResponse
    '''

    return render(request, 'index.html', get_base_context(request))
