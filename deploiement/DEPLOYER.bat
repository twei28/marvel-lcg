@echo off
rem NarwhalChampions : deploie le depot sur le serveur et le redemarre.
rem Equivalent de "clic droit > Executer avec PowerShell" sur deployer.ps1,
rem pour qui ne peut que double-cliquer (poste pilote a distance).
rem Tout ce qui s affiche est aussi ecrit dans dernier-deploiement.log,
rem pour pouvoir relire un refus sans recopier l ecran.
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -Command "& { .\deployer.ps1 %* 2>&1 | Tee-Object -FilePath .\dernier-deploiement.log }"
echo.
echo Deploiement termine. Si la derniere ligne dit "active", relance ta partie.
echo Le detail est dans dernier-deploiement.log.
pause
