#!/bin/bash

nohup /opt/venv_python2.7.13/bin/python manage.py runserver 0.0.0.0:8000 --insecure &
echo $(echo -e "\n")