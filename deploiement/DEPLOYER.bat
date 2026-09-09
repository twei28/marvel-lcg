@echo off
rem NarwhalChampions : deploie le depot sur le serveur et le redemarre.
rem Equivalent de "clic droit > Executer avec PowerShell" sur deployer.ps1,
rem pour qui ne peut que double-cliquer (poste pilote a distance).
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File ".\deployer.ps1" %*
echo.
echo Deploiement termine. Si la derniere ligne dit "active", relance ta partie.
pause
