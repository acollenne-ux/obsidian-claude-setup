@echo off
REM Lance un tunnel Cloudflare pour exposer l'API Obsidian a claude.ai
REM Obsidian doit etre ouvert avec le plugin Local REST API actif

echo === Tunnel Obsidian - claude.ai ===
echo Obsidian Local REST API doit etre actif sur localhost:27124
echo.

REM Verifier que l'API est accessible
curl -s -k https://127.0.0.1:27124/ >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERREUR] API Obsidian non accessible. Ouvre Obsidian d'abord.
    pause
    exit /b 1
)
echo [OK] API Obsidian accessible

REM Lancer cloudflared
where cloudflared >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERREUR] cloudflared non installe.
    echo   Installation: winget install Cloudflare.cloudflared
    pause
    exit /b 1
)

echo [INFO] Lancement du tunnel Cloudflare...
echo [INFO] Copie l'URL affichee ci-dessous et ajoute-la dans claude.ai - Settings - MCP
echo [IMPORTANT] Utilise --no-tls-verify car Obsidian utilise un certificat auto-signe
echo.
cloudflared tunnel --url https://localhost:27124 --no-tls-verify
