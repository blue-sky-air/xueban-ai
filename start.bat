@echo off
chcp 65001 >nul 2>&1

echo ========================================
echo   XueBan AI - Smart Learning Platform
echo ========================================
echo.

echo [1] Installing backend dependencies...
cd /d "%~dp0backend"
pip install -r requirements.txt -q 2>nul

echo [2] Starting backend (port 8000)...
start "XueBan-Backend" cmd /k "chcp 65001 >nul && cd /d "%~dp0backend" && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"

timeout /t 3 /nobreak >nul

echo [3] Installing frontend dependencies...
cd /d "%~dp0frontend"
call npm install --silent 2>nul

echo [4] Starting frontend (port 5173)...
start "XueBan-Frontend" cmd /k "chcp 65001 >nul && cd /d "%~dp0frontend" && npx.cmd vite --host 0.0.0.0 --port 5173"

echo.
echo ========================================
echo   All services started!
echo.
echo   Frontend:  http://localhost:5173
echo   Backend:   http://localhost:8000
echo   API Docs:  http://localhost:8000/docs
echo ========================================
echo.
echo Close this window won't stop the services.
echo To stop: close the XueBan-Backend and XueBan-Frontend windows.
echo.
pause
