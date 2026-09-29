@echo off
REM ===== EVERY MORNING: double-click this =====
cd /d C:\AskIT\dxc-agentic-ai || (echo [!!] Repo not found at C:\AskIT\dxc-agentic-ai & pause & exit /b 1)
echo Getting new content from the trainer...
git fetch -q upstream
git merge -q upstream/main --no-edit
if errorlevel 1 (git merge --abort & echo [!!] Could not update - call the trainer & pause & exit /b 1)
call .venv\Scripts\activate.bat
pip install -q -r requirements.txt
python tools\portal.py
pause
