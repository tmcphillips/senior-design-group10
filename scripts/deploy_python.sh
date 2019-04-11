#!/bin/sh
cd ..
pip install -r requirements.txt
cd ./yw_website/

python manage.py makemigrations
python manage.py migrate 
python manage.py makemigrations website
python manage.py migrate website
# python manage.py create_test_database
python manage.py rebuild_index --noinput
python manage.py test
python manage.py runserver
