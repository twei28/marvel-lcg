@echo off
title Marvel Champions - partie multijoueur
echo Demarrage de la partie multijoueur...
echo (laisse cette fenetre ouverte pendant toute la partie)
echo.
wsl.exe -e bash -lc "cd '/mnt/c/Users/arnau/Desktop/Marvel LCG/Fusion/marvel-lcg-src' && ./launcher-multi.sh"
echo.
echo Partie terminee.
pause
