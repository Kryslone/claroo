web: gunicorn claroo.wsgi --log-file - 
#or works good with external database
web: python manage.py migrate && gunicorn claroo.wsgi