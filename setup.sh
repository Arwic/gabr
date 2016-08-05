#!/bin/bash

sudo apt-get install python3 python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx
sudo pip3 install virtualenv
virtualenv gabrenv
. gabrenv/bin/activate
pip3 install django python-dateutil pillow gunicorn psycopg2 django-nocaptcha-recaptcha django-axes