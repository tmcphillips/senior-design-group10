#!/bin/bash
echo "Copying files to server..."
scp -r ../../senior-design-group10/ clundin@workflow-web.gonzaga.edu:.
ssh -t clundin@workflow-web.gonzaga.edu << EOF
cd ./senior-design-group10/
pip3 install -r requirements.txt
cd ./yw_website/
python3 manage.py makemigrations
python3 manage.py migrate 
python3 manage.py test
sudo python3 manage.py runserver https://147.222.165.82:80&
EOF
