@echo off
call .\venv\Scripts\activate
python validate.py
deactivate
pause