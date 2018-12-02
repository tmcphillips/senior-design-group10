#!/bin/sh
cd ..
pip3 install -r requirements.txt
cd ./yw_website/

python3 manage.py makemigrations
python3 manage.py migrate 
python3 manage.py create_test_database
python3 manage.py test
python3 manage.py runserver
