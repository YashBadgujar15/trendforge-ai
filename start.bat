@echo off
title TrendForge AI — Team AgentX Launcher
color 0b
echo ========================================================
echo   TRENDFORGE AI -- AUTONOMOUS CONTENT STUDIO
echo   Team AgentX (Yash Badgujar, Anjali Sonar, Pranav Jogi)
echo   SCET Surat -- AI Build Challenge 2026 (PS-02)
echo ========================================================
echo.

set DIR=%~dp0
cd /d "%DIR%"

set PY=python
if exist "%DIR%backend\venv\Scripts\python.exe" set PY="%DIR%backend\venv\Scripts\python.exe"

echo [1/3] Starting Backend API Server (Port 8000)...
start "TrendForge AI - Backend" cmd /k "cd /d "%DIR%backend" && %PY% main.py"

echo [2/3] Starting Frontend Web Server (Port 5501)...
start "TrendForge AI - Frontend" cmd /k "cd /d "%DIR%" && %PY% serve.py"

echo [3/3] Opening TrendForge AI in Browser...
timeout /t 2 >nul
start http://127.0.0.1:5501

echo.
echo ========================================================
echo TrendForge AI is LIVE!
echo Frontend: http://127.0.0.1:5501
echo Backend:  http://127.0.0.1:8000
echo ========================================================
echo.
