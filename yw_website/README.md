# Prerequisites
In order to run website make sure you have installed:
* python3
* pip for python3
* Django for python3


If you don't have these programs:
On a Linux-debian distro, enter 
```bash
sudo apt install python3 into the terminal
```
On a Mac, use home brew's
```bash
brew install python3
```

Once python3 is installed, install pip
Mac should have this installed by default
```bash
sudo apt-get install python3-pip
```
Next, from the terminal enter
```bash
pip3 install Django
```
Now you have all the current dependencies for our website.

# Running the website
At the project root directory, Enter into the terminal
```bash
python3 manage.py runserver
```

By default the website will run at http://127.0.0.1:8000 but
the terminal will output if the port changed. With your webbrowser, navigate to the url outputted by the terminal.

# Future file structure
Our project structure to reflect this suggested project structure found at:
https://stackoverflow.com/questions/22841764/best-practice-for-django-project-working-directory-structure 

```python
~/projects/project_name/

docs/               # documentation
scripts/
  manage.py         # installed to PATH via setup.py
project_name/       # project dir (the one which django-admin.py creates)
  apps/             # project-specific applications
    accounts/       # most frequent app, with custom user model
    __init__.py
    ...
  settings/         # settings for different environments, see below
    __init__.py
    production.py
    development.py
    ...

  __init__.py       # contains project version
  urls.py
  wsgi.py
static/             # site-specific static files
templates/          # site-specific templates
tests/              # site-specific tests (mostly in-browser ones)
tmp/                # excluded from git
setup.py
requirements.txt
requirements_dev.txt
pytest.ini
...
```
