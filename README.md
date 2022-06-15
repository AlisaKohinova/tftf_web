# tftf_web

## Setup

You need python (version > 3.) and pip to be installed on your system. 
https://www.python.org/downloads/
https://pip.pypa.io/en/stable/installation/

The first thing to do is to clone the repository:

```sh
$ git clone git@github.com:AlisaKoginova/tftf_web.git
$ cd tftf_web
```

Create a virtual environment to install dependencies in and activate it (This part depends on the system you are working to, it is usually better to initialize virtual environment, but if you have troubles with it - just skip this step):

```sh
$ virtualenv2 --no-site-packages env
$ source env/bin/activate
```
Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv2`.

Once `pip` has finished downloading the dependencies:
```sh
(env)$ cd tftf
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/`.
