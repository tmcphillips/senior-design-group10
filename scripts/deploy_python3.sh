#!/bin/sh
# Note: If running on a windows device, change python3 to python
# All of these commands should be run in python3 but the default python
# for UNIX-based devices like MacOS and Linux default to python2

cd ..
pip3 install -r requirements.txt
cd ./yw_website/

python3 manage.py makemigrations # Migrate django tables
python3 manage.py migrate 
python3 manage.py makemigrations website # Migrate yesworkflow-web tables
python3 manage.py migrate website
# python3 manage.py create_test_database # Uncomment to populate database with 
# Latin dummy data
python3 manage.py rebuild_index --noinput # Index data in database for search API
python3 manage.py test
python3 manage.py runserver
