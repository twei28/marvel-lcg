@echo off
rem NarwhalChampions : redemarre le site et TOUS les moteurs de table.
rem Les parties en cours sont perdues. A double-cliquer, rien a taper.
rem Meme commande que le MODE-EMPLOI (section "Redemarrer").
cd /d "%~dp0"
echo Redemarrage du serveur NarwhalChampions...
ssh -i cle_narwhal -o StrictHostKeyChecking=accept-new root@178.105.177.39 "systemctl restart narwhal && sleep 3 && systemctl is-active narwhal"
echo.
echo Si la ligne au-dessus dit "active", c est bon : relance ta partie.
pause
