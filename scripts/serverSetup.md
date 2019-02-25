# Getting started with YesWorkflow Web Components

**Please ensure that JDK 10 and Maven 3+ are installed on your machine before continuing and confirm that JDK 10 is your default JAVA_HOME**

## Deploying the web sever
In the yw_website directory, change directory into the scripts directory. You should see a number of bash scripts:
```
deploy_python.sh
deploy_python3.sh
remote_deploy_python.sh
remote_deploy_python3.sh
workflow_sample.gv
```
If you would like to deploy a test server on your localhost, you may run one of these two files:
```
deploy_python.sh
deploy_python3.sh
```
For windows users, use deploy_python.sh

For Mac/Linux users, use deploy_python3.sh

These scripts will deploy a web server running on your local machine at 
```http://localhost:8000```

Deploying on a remote web server is a bit trickier because we will need
to edit our remote deploy scripts. Let's take a look at ```remote_deploy_python3.sh```

```
#!/bin/bash
echo "Copying files to server..."
scp -r ../../senior-design-group10/ clundin@workflow-web.gonzaga.edu:.
ssh -t clundin@workflow-web.gonzaga.edu << EOF
cd ./senior-design-group10/
pip3 install -r requirements.txt
cd ./yw_website/
python3 manage.py makemigrations
python3 manage.py migrate 
python3 manage.py makemigrations website
python3 manage.py migrate website
python3 manage.py test
sudo python3 manage.py runserver https://147.222.165.82:80&
EOF
```

Here we are ssh-ing into our webserver at 
workflow-web.gonzaga.edu and running our deploy scripts.
Additionally, the IP address at the bottom of the script 
is also given. We'll change these to reflect our own web server and now run the script.

When the server is up and running, navigate to the login page and create an account. This account will be used for uploading later.

## Uploading a workflow
If you are unfamiliar with how the YesWorkflow CLI works or how to write a workflow, take a look at the readme [here.](https://github.com/yesworkflow-org/yw-prototypes)

Saving a workflow to the webserver follows much of the same syntax as running any other command in the CLI. We do however need to provide a few extra things to upload properly. To see a list of all compatible config options using yw save, run 
```
yw -h
``` 
Assuming that we have an alias set for the YW Jar file:

```
yw save <path-to-workflow-script> -c save.serveraddress=<server dns> -c save.username=<username> -c save.title=<workflow-title> -c save.description=<workflow-description> -c save.tags=<comma-separated-string-of-tags>-c graph.dotfile=<path-to-dump-graph-output>
```

If we run this in the command line given the proper inputs, we will have uploaded our first script to the server! Check your server's web page and there should be an entry with the given workflow's script. Keep in mind that giving a path for the dotfile is optional and only serves to clean up command line output.