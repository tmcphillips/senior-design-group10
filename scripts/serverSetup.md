# Getting started with YesWorkflow Web Components

**Please ensure that JDK 10 is installed on your machine before continuing and confirm that JDK 10 is your default JAVA_HOME. Additionally, this system uses either Python 3.5 or 3.6.**

## Deploying the web sever
In the yw_website directory, change directory into the scripts directory. You should see a number of bash scripts:
```
deploy_python.sh
deploy_python3.sh
workflow_sample.gv
```
# Deploy locally
If you would like to deploy a test server on your localhost, first ensure that you're not running anything on port 8000, then you may run one of these two files:
```
deploy_python.sh
deploy_python3.sh
```
For windows users, use deploy_python.sh

For Mac/Linux users, use deploy_python3.sh

These scripts will deploy a web server running on your local machine at 
```http://localhost:8000```

When the server is up and running, navigate to the login page and create an account. This account will be used for uploading later.

# Deploy on a remote server
The steps for deploying on a remote are similar to deploying locally, but require that you ssh into your web server. Our personal web server is deployed on a machine running Ubuntu 18.04.1 LTS.

Assuming that you have used scp to transfer this repository onto your web server, we can run these commands from the root directory of the repository:
```
pip3 install -r requirements.txt
cd ./yw_website/
python manage.py makemigrations
python manage.py migrate 
python manage.py makemigrations website
python manage.py migrate website
python manage.py test
sudo python manage.py runserver <server_ip>
```
Simply replace server_ip with the ip address of your web server and you should be up and running!

## Uploading a workflow
If you are unfamiliar with how the YesWorkflow CLI works or how to write a workflow, take a look at the readme [here.](https://github.com/yesworkflow-org/yw-prototypes) Additionally, please follow the link for documentation surrounding YesWorkflow Save [here.](https://github.com/aniehuser/senior-design-group10#using-the-yesworkflow-save-cli-command)

Saving a workflow to the webserver follows much of the same syntax as running any other command in the CLI. We do however need to provide a few extra things to upload properly. To see a list of all compatible config options using yw save, run 
```
yw -h
``` 
Following the YesWorkflow save documentation will explain how the command works in the CLI. If your web server is up and running, try saving a workflow by following the instructions on the documentation.