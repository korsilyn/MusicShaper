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
