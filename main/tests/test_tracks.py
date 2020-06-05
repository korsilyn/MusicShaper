'''
Модуль тестирования безопасности трека
'''

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class TrackTestCase(TestCase):
    '''
    Класс, тестирующий доступ пользлователя к треку
    '''

    fixtures = ['basic.json']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username='liza')
        self.client.force_login(user=self.user)

    def test_track_public_access(self):
        '''
        Проверка доступа к общедоступному треку
        '''

        response = self.client.get(reverse('track', kwargs={'track_id': 1}))
        self.assertEqual(response.status_code, 200)

    def test_track_link_access(self):
        '''
        Проверка доступа к треку по ссылке
        '''

        response = self.client.get(reverse('track', kwargs={'track_id': 2}))
        self.assertEqual(response.status_code, 200)

    def test_track_private_access(self):
        '''
        Проверка доступа к приватному треку
        '''

        response = self.client.get(reverse('track', kwargs={'track_id': 3}))
        self.assertEqual(response.status_code, 404)