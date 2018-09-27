In order to run website make sure you have:
Installed python3
Installed pip for python3
Installed Django for python3

If you don't have these programs:
On a Linux-debian distro, enter sudo apt install python3 into the terminal
On a Mac, use home brew's brew install python3

Once python3 is installed
run 
sudo apt-get install python3-pip
To install pip. On Mac this should be installed by default.

Next, from the terminal enter
pip3 install Django

Now you have all the current dependencies for our website.

At the project root directory, Enter into the terminal
python3 manage.py runserver

By default the website will run at http://127.0.0.1:8000/yw_root but
the terminal will output if the port changed. With your webbrowser, navigate to the url outputted by the terminal, with /yw_root appended to the end.
