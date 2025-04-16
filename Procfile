release: uv run manage.py migrate
web: uv run manage.py runserver 0.0.0.0:8000 
worker: uv run celery -A devproject worker --loglevel=info