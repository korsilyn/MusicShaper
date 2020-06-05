'''
Модуль тестирования присутсвия только публичных треков на страницы популярных треков
'''

from django.test import Client, TestCase
from django.urls import reverse
from ..models import TrackSettings


class PopularTrackTestCase(TestCase):
    '''
    Класс, тестирующий публичность треков на странице популярных треков
    '''

    fixtures = ['basic.json']

    def setUp(self):
        self.client = Client()

    def test_public_popular_tracks(self):
        '''
        Проверка публичности всех на странице "популярное"
        '''

        response = self.client.get(reverse('popular_tracks'))
        tracks = response.context['tracks']
        self.assertTrue(all(TrackSettings.objects.filter(track__id=track['id'], access=2).exists() for track in tracks))
