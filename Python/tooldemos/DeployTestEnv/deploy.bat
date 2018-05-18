@echo off
cd %~dp0

fab -f batch_update.py start

pause
