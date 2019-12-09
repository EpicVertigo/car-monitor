server:
	python manage.py runserver

celery:
	celery -A carmonitor worker --loglevel=info

celery-beat:
	celery -A carmonitor beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

flower:
	flower -A carmonitor --port=5555

shell:
	python manage.py shell

collectstatic:
	python manage.py collectstatic --noinput

gunicorn:
	gunicorn -b 0.0.0.0:8000 carmonitor.wsgi:application

run: collectstatic gunicorn