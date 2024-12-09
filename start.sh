#!/bin/bash

start gunicorn myproject.wsgi:application --bind 0.0.0.0:$PORT
start python manage.py launch_telegram_bot
start python manage.py qcluster

