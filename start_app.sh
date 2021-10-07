#!/bin/bash
sleep 5s

python manage.py check
python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8020