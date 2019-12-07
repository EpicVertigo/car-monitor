server:
	python manage.py runserver

celery:
	celery -A carmonitor worker --loglevel=info

celery-beat:
	celery -A carmonitor beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler