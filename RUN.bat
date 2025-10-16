@echo off
cls
echo ========================================
echo  XML Sender - Iniciando aplicacao...
echo ========================================
echo.

REM Ativar o ambiente virtual
call venv_sender\Scripts\activate.bat

REM Executar a aplicacao
python main.py

pause

