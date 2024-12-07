web: gunicorn panda_records_api.wsgi:application --log-level=debug
worker_qcluster: python manage.py qcluster
worker_telegram_bot: python manage.py launch_telegram_bot
