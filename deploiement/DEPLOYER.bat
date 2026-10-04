@echo off
rem NarwhalChampions : construit le plateau, deploie le depot sur le serveur et le redemarre.
rem Equivalent de "clic droit > Executer avec PowerShell" sur deployer.ps1,
rem pour qui ne peut que double-cliquer (poste pilote a distance).
rem Le journal dernier-deploiement.log est tenu par deployer.ps1 lui-meme
rem depuis le 16/09/2026 : il etait auparavant ecrit ICI, et personne
rem n utilisant plus ce .bat, il datait de cinq jours tout en ayant l air a
rem jour. La construction du plateau ci-dessous ecrit dans
rem construction-plateau.log : deployer.ps1 ouvre son journal par
rem Start-Transcript -Force, qui l aurait efface.
cd /d "%~dp0"
echo == Construction du plateau (ui-app/deployer.sh, dans WSL)
rem Sans cette etape, deployer.ps1 envoie le plateau tel qu il a ete construit
rem la derniere fois : un correctif commite mais jamais construit n arriverait
rem pas sur le serveur (constate le 09/09/2026). Le chemin est celui de la
rem copie vivante, code en dur comme dans deployer.ps1 (etape des scans).
rem Un SCRIPT et non une ligne de commande : cmd, wsl et bash se disputent
rem les guillemets, et « Marvel LCG » avec son espace n y survivait pas.
wsl -e bash -l "/mnt/c/Users/arnau/Desktop/Marvel LCG/deploiement/construire-plateau.sh" > construction-plateau.log 2>&1
if errorlevel 1 (
  echo La construction du plateau a echoue. Voir construction-plateau.log.
  pause
  exit /b 1
)
type construction-plateau.log | findstr /i "built Deploye"
echo == Envoi vers le serveur
rem SANS redirection ni Tee-Object (03/10/2026). Sous Windows PowerShell,
rem `2>&1` change chaque ligne d erreur standard d un programme natif en
rem erreur PowerShell ; deployer.ps1 tourne en ErrorActionPreference Stop, et
rem le simple avertissement de tar (LIBARCHIVE.symlinktype) arretait tout a
rem l extraction. Le journal est deja tenu par deployer.ps1 (Start-Transcript).
powershell -NoProfile -ExecutionPolicy Bypass -File .\deployer.ps1 %*
echo.
echo Deploiement termine. Si la derniere ligne dit "active", recharge ta partie.
echo Le detail est dans dernier-deploiement.log.
pause
