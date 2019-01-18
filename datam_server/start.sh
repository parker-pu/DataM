celery worker -A datam_server -l info &
celery -A datam_server beat -l info  --scheduler django_celery_beat.schedulers:DatabaseScheduler &
python ./manage.py runserver 0.0.0.0:8080 &