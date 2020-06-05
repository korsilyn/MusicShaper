'''
========================================
Модуль тестирования *безопасности* сайта
========================================
'''

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class AdminTestCase(TestCase):
    '''
    **Класс, тестирующий отсутствие доступа обычного
    пользователя к функциям админов**
    '''

    fixtures = ['basic.json']

    def login(self, username):
        '''
        Впомогательная функция для авторизации
        '''

        self.user = User.objects.get(username=username)
        self.client.force_login(self.user)

    def setUp(self):
        self.client = Client()
        self.user = None

    def test_normal_user_home(self):
        '''
        Тест редиректа обычного пользователя со страницы `admin_home`
        '''

        self.login('liza')
        response = self.client.get(reverse('admin_home'))
        self.assertEqual(response.status_code, 302)

    def test_admin_home(self):
        '''
        Тест пропуска админа
        '''

        self.login('vasya')
        response = self.client.get(reverse('admin_home'))
        self.assertEqual(response.status_code, 200)
