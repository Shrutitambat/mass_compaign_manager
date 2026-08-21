@echo off
title Campaign Manager Launcher
echo Starting Redis, Celery, and Django...

:: 1. Launch Redis Server in background
start "Redis Server" C:\Redis\redis-server.exe

:: 2. Launch Celery Worker in a new window
start "Celery Worker" cmd /k "call venv\Scripts\activate && celery -A mass_campaign_manager worker -l info -P solo"

:: 3. Launch Django Server in a new window
start "Django Web Server" cmd /k "call venv\Scripts\activate && python manage.py runserver"

echo All services are running!