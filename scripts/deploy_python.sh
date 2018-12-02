#!/bin/sh
cd ..
pip install -r requirements.txt
cd ./yw_website/

python manage.py makemigrations
python manage.py migrate 
python manage.py create_test_database
python manage.py test
python manage.py runserver
