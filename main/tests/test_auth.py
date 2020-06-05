'''
===============================
Модуль тестирования авторизации
===============================
'''

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Profile


class AuthTestCase(TestCase):
    '''
    **Класс, тестирующий авторизацию на сайте**
    '''

    fixtures = ['basic.json']

    def setUp(self):
        self.client = Client()
        user = User.objects.get(username='vasya')
        user.set_password('promprog')
        user.save()

    def test_login(self):
        '''
        Тест авторизации
        '''

        credentials = {
            'username': 'vasya',
            'password': 'promprog',
        }

        response = self.client.post(reverse('login'), credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_register(self):
        '''
        Тест регистрации
        '''

        password = 'progprom'
        credentials = {
            'username': 'megavasya',
            'password1': password,
            'password2': password,
        }

        response = self.client.post(reverse('register'), credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertTrue(hasattr(response.context['user'], 'profile'))

    def test_logout(self):
        '''
        Тест деавторизации
        '''

        user = User.objects.get(username='vasya')
        self.client.force_login(user)
        response = self.client.get(reverse('logout'), {}, follow=True)
        self.assertTrue(response.context['user'].is_anonymous)

    def test_profile_creation(self):
        '''
        Тест создания профиля для нового пользователя
        (через django signals)
        '''

        new_user = User.objects.create_user(
            username='hypervasya',
            password='prompromprog'
        )

        self.assertTrue(Profile.objects.filter(user=new_user).exists())
        self.assertTrue(hasattr(new_user, 'profile'))
