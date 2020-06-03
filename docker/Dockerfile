FROM python:3.7
MAINTAINER Andrew Smirnov <smirnov@informatics.ru>
ADD ./ /s106_ms
WORKDIR /s106_ms/
CMD exec apt-get update
CMD exec apt-get install build-essential nano python3-dev libmysqlclient-dev
RUN pip install --no-cache-dir -r ./requirements.txt
ENV DJANGO_DB_NAME=default
ENV DJANGO_SU_NAME=admin
ENV DJANGO_SU_PASSWORD=adminpass

RUN python -c "import django, os, sys; sys.path.insert(0, os.path.abspath('.')); \
    os.environ['DJANGO_SETTINGS_MODULE'] = 'MusicShaper.settings'; django.setup(); \
    from django.contrib.auth.management.commands.createsuperuser import get_user_model; \
    get_user_model()._default_manager.db_manager('$DJANGO_DB_NAME').create_superuser( \
    username='$DJANGO_SU_NAME', \
    password='$DJANGO_SU_PASSWORD')"
   
CMD exec ./docker/run.sh
