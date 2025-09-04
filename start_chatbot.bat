@echo off
echo Starting Chatbot...

REM Stop any existing processes first
call stop_chatbot.bat

REM Wait for 2 seconds to ensure ports are freed
timeout /t 2 /nobreak

REM Start the action server in a new window
start "Rasa Action Server" cmd /k "cd %~dp0 && .\venv\Scripts\activate && rasa run actions"

REM Wait for 5 seconds to ensure action server is up
timeout /t 5 /nobreak

REM Start the Rasa shell in the current window
.\venv\Scripts\activate
rasa shell

echo Chatbot started successfully! 