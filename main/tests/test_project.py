'''
Модуль тестирования создания проекта
'''

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from ..models import MusicTrackProject


class ProjectTestCase(TestCase):
    '''
    Класс, тестирующий правильность создания проекта
    '''

    fixtures = ['basic.json']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username='vasya')
        self.client.force_login(user=self.user)

    def test_project_creation(self):
        '''
        Тест создания проекта и его существования
        '''

        credentials = {
            'name': 'TestProject',
            'decs': 'testing project creation',
        }
        self.client.post(reverse('new_project'), credentials, follow=True)
        self.assertTrue(MusicTrackProject.objects.filter(name='TestProject').exists())