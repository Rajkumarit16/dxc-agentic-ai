@echo off
REM ===== BACKUP ONLY: use if the Day End button did not work =====
cd /d C:\AskIT\dxc-agentic-ai
call .venv\Scripts\activate.bat
python tools\day_end.py %1
pause
