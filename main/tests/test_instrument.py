'''
Модуль тестирования создания инструмента
'''

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from ..models import MusicInstrument


class InstrumentTestCase(TestCase):
    '''
    Класс, тестирующий правильность создания инструмента
    '''

    fixtures = ['basic.json']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username='vasya')
        self.client.force_login(user=self.user)

    def test_instrument_creation(self):
        '''
        Тест создания инструмента и его существования
        '''

        credentials = {
            'name': 'TestInstrument',
            'type': 'Synth',
            'notesColor': '#ff0000',
        }

        self.client.post(reverse('new_instrument', kwargs={'proj_id': 1}), credentials, follow=True)
        self.assertTrue(MusicInstrument.objects.filter(name='TestInstrument').exists())
