web: gunicorn backend.admin.wsgi
release: python backend.manage.py makemigrations --noinput
release: python backend.manage.py collectstatic --noinput
release: python backend.manage.py migrate --noinput
