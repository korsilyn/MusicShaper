# Music Shaper

Music Shaper позволяет вам легко писать собственные композиции и делиться ими со всем миром!

## Давайте начнем

Эти инструкции позволят вам установить проект на свой ПК

### Требования

Что требуется для работы проекта

```
python3 # Tested on 3.8.3rc1
Django==3.0 # Tested on 3.0.6
Pillow==7.0.0
django-jsonfield==1.4.0
```

### Установка

Эти шаги покажут как установить наш проект на ваш ПК

```
python3 -m venv venv
. venv/bin/activate # Unix-like
./venv/Scripts/activate # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Поздравляем! Сервер запущен! (но это не точно)


## Работает при помощи

* [Django](https://docs.djangoproject.com/en/3.0/) - Бэкенд фреймворк
* [Bootstrap 4](https://getbootstrap.com/docs/4.4/) - Дизайн
* [Pillow](https://pillow.readthedocs.io/en/stable/) - Обработка картинок
* [Tone.js](https://tonejs.github.io/) - Воспроизведение звука в браузере
* [Paper.js](http://paperjs.org/) - Отрисовка редактора нот

### Паттерны

* MVT (Model-View-Template) - Django
* Шаблонный метод - все страницы наследуются от `base.html`
* Стратегия - для удаления проектов / паттернов / автара используется один шаблон `delete.html`
* Стратегия - Все модели, хранящие настройки, наследуются от абстрактной модели `ModelWithSettings`
* Контейнер свойств - модель `ModelWithSettings` (объекты модели хранят настройки как аттрибуты)
* Отложенная инициализация - модель `ModelWithSettings` (объекты хранят только изменения)
* Делегирование - поля настроек модели `ModelWithSettings` реализуют абстрактный класс `SettingValue`

## Авторы

* **Петр Костенко** - *Тимлид* - [Picalines](https://github.com/Picalines)
* **Мария Давыдова** - *Менеджер Проекта* - [marussyyaa](https://gitlab.informatics.ru/marussyyaa)
* **Илья Сасин** - *Кодер* - [unicorn-deadinside](https://gitlab.informatics.ru/unicorn-deadinside)
* **Евгений Гладков** - *Кодер* - [korsilyn](https://github.com/korsilyn)
* **Даниил Гиль** - *Дизайнер* - [Tintie](https://gitlab.informatics.ru/Tintie)
