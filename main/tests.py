'''
Модуль тестирования (unittest) сайта
'''

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

print('rabotaet')


class LoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def check_if_loads(self, url):
        response = self.client.get(reverse(url))
        self.assertEqual(response.status_code, 200)
        return response

    def test_if_mainpage_loads(self):
        self.check_if_loads('index')

    def test_if_profile_loads(self):
        self.check_if_loads('profile')

    def test_if_populartracks_loads(self):
        self.check_if_loads('popular_tracks')

    def test_if_track_loads(self):
        self.check_if_loads('track')
