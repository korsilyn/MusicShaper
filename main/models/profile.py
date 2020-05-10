'''
Модуль модели профиля пользователя
'''

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    '''
    Модель профиля

    :param user: имя проекта
    :param desc: описание
    :param author: автор
    :param patterns: список паттернов
    :param data: файл с данными проекта (настройки, инструменты и т.д.)
    '''

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='', upload_to='profile_pics')
    status = models.CharField(max_length=100, default='')
    subscribers = models.ManyToManyField("Profile")

    def to_dict(self):
        '''
        Переводит модель профиля в словарь
        (поле image считается за url файла)

        :rtype: dict
        '''

        return {
            'id': self.pk,
            'image': self.image.url if self.image else None,
            'status': self.status,
        }


def create_profile(sender, **kwargs):
    '''
    Обработчик сигнала, который срабатывает при создании
    модели User (нужно для автоматической связи User и Profile)
    '''

    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)


def user_to_dict(user: User):
    '''
    Переводит модель пользователя в словарь

    :param user: модель пользователя
    :rtype: dict
    '''

    return {
        'id': user.pk,
        'username': user.username,
        'profile': user.profile.to_dict(),
    }
