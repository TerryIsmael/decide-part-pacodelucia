#!/bin/sh
cd decide/
cp local_settings.deploy.py local_settings.py
./manage.py createsuperuser --noinput
./manage.py collectstatic --noinput
./manage.py makemigrations
./manage.py migrate