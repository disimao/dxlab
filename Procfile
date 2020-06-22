release: python manage.py migrate --noinput && python manage.py loaddata dxlab/apps/core/fixtures/fixtures.json
web: gunicorn dxlab.wsgi