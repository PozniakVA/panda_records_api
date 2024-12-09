web: gunicorn panda_records_api.wsgi:application --bind 0.0.0.0:$PORT
qcluster: python manage.py qcluster
bot: python manage.py launch_telegram_bot