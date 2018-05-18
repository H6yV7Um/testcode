@echo off
cd %~dp0

fab -f recovery_cluster.py deploy

pause
