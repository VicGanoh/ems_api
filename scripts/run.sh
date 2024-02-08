#! bin/sh

set -e

python manage.py collectstatic --noinput
python manage.py makemigrations account employees project task commons
python manage.py collecstatic --noinput
python manage.py migrate --noinput

uwsgi --socket :9000 --workers 4 --master --enable-threads --module config.wsgi