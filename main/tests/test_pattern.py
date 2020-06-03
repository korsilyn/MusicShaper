'''
Модуль тестирования создания паттерна
'''

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from ..models import MusicTrackPattern


class PatternTestCase(TestCase):
    '''
    Класс, тестирующий правильность создания паттерна
    '''

    fixtures = ['basic.json']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username='liza')
        self.client.force_login(user=self.user)

    def test_pattern_creation(self):
        '''
        Тест создания паттерна и его существования
        '''

        credentials = {
            'color': '#00ffff',
            'name': 'TestPattern',
            'duration': 200,
        }

        self.client.post(reverse('new_pattern', kwargs={'proj_id': 2}), credentials, follow=True)
        self.assertTrue(MusicTrackPattern.objects.filter(name='TestPattern').exists())
