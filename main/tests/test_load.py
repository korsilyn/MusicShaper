'''
Модуль тестирования (unittest) сайта
'''

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class LoginTestCase(TestCase):
    '''
    Класс, тестирующий загрузку основгых страниц и проверку login_required
    '''

    fixtures = ['basic.json']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username='vasya')
        self.client.force_login(user=self.user)

    def check_if_loads(self, url, get_args='', **kwargs):
        response = self.client.get(reverse(url, kwargs=kwargs) + '?' + get_args)
        self.assertEqual(response.status_code, 200)
        return response

    def check_login_required(self, url, should_error, get_args='', **kwargs):
        self.client.logout()
        response = self.client.get(reverse(url, kwargs=kwargs) + '?' + get_args)
        self.assertEqual(response.status_code, 302 if should_error else 200)
        return response

    def test_mainpage_loads(self):
        self.check_if_loads('index')
        self.check_login_required('index', False)

    def test_profile_loads(self):
        self.check_if_loads('profile')
        self.check_login_required('profile', True)

    def test_others_profile_loads(self):
        self.check_login_required('profile', False, 'username=vasya')

    def test_populartracks_loads(self):
        self.check_if_loads('popular_tracks')
        self.check_login_required('popular_tracks', False)

    def test_track_loads(self):
        self.check_if_loads('track', track_id=1)
        self.check_login_required('track', False, track_id=1)

    def test_projects_load(self):
        self.check_if_loads('projects')
        self.check_login_required('projects', True)

    def test_login_loads(self):
        self.check_if_loads('login')
        self.check_login_required('login', False)

    def test_register_loads(self):
        self.check_if_loads('register')
        self.check_login_required('register', False)

    def test_logout_loads(self):
        response = self.client.get('logout')
        self.assertEqual(response.status_code, 404)
        self.check_login_required('logout', True)

    def test_profile_edit_loads(self):
        self.check_if_loads('profile_edit')
        self.check_login_required('profile_edit', True)

    def test_delete_avatar_loads(self):
        self.check_if_loads('delete_avatar')
        self.check_login_required('delete_avatar', True)

    def test_change_password_loads(self):
        self.check_if_loads('change_password')
        self.check_login_required('change_password', True)

    def test_new_project_loads(self):
        self.check_if_loads('new_project')
        self.check_login_required('new_project', True)

    def test_project_home_loads(self):
        self.check_if_loads('project_home', proj_id=1)
        self.check_login_required('project_home', True, proj_id=1)

    def test_manage_project_loads(self):
        self.check_if_loads('manage_project', proj_id=1)
        self.check_login_required('manage_project', True, proj_id=1)

    def test_delete_project_loads(self):
        self.check_if_loads('delete_project', proj_id=1)
        self.check_login_required('delete_project', True, proj_id=1)

    def test_new_instruments_loads(self):
        self.check_if_loads('new_instrument', proj_id=1)
        self.check_login_required('new_instrument', True, proj_id=1)

    def test_edit_instrument_loads(self):
        self.check_if_loads('edit_instrument', proj_id=1, instr_id=1)
        self.check_login_required('edit_instrument', True, proj_id=1, instr_id=1)

    def test_manage_instrument_loads(self):
        self.check_if_loads('manage_instrument', proj_id=1, instr_id=1)
        self.check_login_required('manage_instrument', True, proj_id=1, instr_id=1)

    def test_delete_instrument_loads(self):
        self.check_if_loads('delete_instrument', proj_id=1, instr_id=1)
        self.check_login_required('delete_instrument', True, proj_id=1, instr_id=1)

    def test_instruments_loads(self):
        self.check_if_loads('instruments', proj_id=1)
        self.check_login_required('instruments', True, proj_id=1)

    def test_search_loads(self):
        self.check_if_loads('search')
        self.check_login_required('search', False)

    def test_admin_create_tests_loads(self):
        self.check_if_loads('create_test_track')
        self.check_login_required('create_test_track', True)

    def test_admin_loads(self):
        self.check_if_loads('admin_home')
        self.check_login_required('admin_home', True)
