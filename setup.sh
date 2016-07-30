#!/bin/bash

sudo apt-get install python3 python3-dev
sudo pip3 install virtualenv
virtualenv gabrenv
. gabrenv/bin/activate
pip3 install django