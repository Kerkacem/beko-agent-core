@echo off
cd /d D:\\beko-agent-core
call .venv\\Scripts\\activate
python beko-agent-main.py
echo %date% %time% >> auto/hourly.log