#!/bin/bash
echo "Copying files to server..."
scp -r ../../senior-design-group10/ clundin@workflow-web.gonzaga.edu:.
ssh -t clundin@workflow-web.gonzaga.edu << EOF
cd ./senior-design-group10/
pip3 install -r requirements.txt
cd ./yw_website/
python manage.py makemigrations
python manage.py migrate 
python manage.py makemigrations website
python manage.py migrate website
python manage.py test
sudo python manage.py runserver https://147.222.165.82:80&
EOF
