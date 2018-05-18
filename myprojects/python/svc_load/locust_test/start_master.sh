#!/bin/bash
#nohup /opt/venv_python2.7.13/bin/locust -f startload.py --master --no-reset-stats > /opt/svc_load/webapp/log/locust_master.log 2>&1 &
nohup /opt/pyvenv36/bin/locust -f startload.py --master --no-reset-stats > /opt/svc_load/webapp/log/locust_master.log 2>&1 &
echo $(echo -e "\n")