@echo off
title Claude Email Bridge

:: Tuer les instances precedentes
wmic process where "name='python.exe' and commandline like '%%email_trigger%%'" delete >nul 2>&1
timeout /t 1 /nobreak >nul

echo.
echo ==========================================
echo   Claude Email Bridge - Actif
echo ==========================================
echo.
echo Surveillance de acollenne@gmail.com...
echo.
echo Depuis votre telephone, envoyez un email a :
echo   acollenne@gmail.com
echo.
echo Sujet : "Claude: votre demande"
echo    ou : "? votre question"
echo    ou : "analyse: Apple AAPL"
echo    ou : "code: script Python pour..."
echo.
echo Vous recevrez la reponse + PDF en retour par email.
echo.
echo NE PAS FERMER CETTE FENETRE. (Minimiser est OK)
echo ==========================================
echo.

cd /d "C:\Users\Alexandre collenne\.claude\tools"
python email_trigger.py
pause
