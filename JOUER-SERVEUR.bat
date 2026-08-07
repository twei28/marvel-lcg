@echo off
title Marvel Champions - serveur pour les amis
echo Demarrage du serveur...
echo (laisse cette fenetre ouverte : les liens ne marchent que pendant ce temps)
echo.
wsl.exe -e bash -lc "cd '/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src' && bash launcher-serveur.sh"
echo.
echo Serveur arrete.
pause
