#!/bin/bash
#nohup /opt/venv_python2.7.13/bin/locust -f startload.py --slave --no-reset-stats --master-host=$1 > /dev/null 2>&1 &
nohup /opt/pyvenv36/bin/locust -f startload.py --slave --no-reset-stats --master-host=$1 > /dev/null 2>&1 &
echo $(echo -e "\n")