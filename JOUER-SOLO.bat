@echo off
title Marvel Champions - partie solo

rem Un jeu tourne-t-il deja sur le port 2345 ? Si oui, inutile d'en lancer un
rem second : le port serait refuse et la fenetre se fermerait sans rien dire.
rem On ouvre le navigateur sur la partie existante a la place.
curl.exe -s -o NUL --max-time 3 http://127.0.0.1:2345/
if %errorlevel%==0 goto DEJA_LANCE

echo Demarrage de la partie solo...
echo (laisse cette fenetre ouverte pendant toute la partie)
echo.
wsl.exe -e bash -lc "cd '/mnt/c/Users/arnau/Desktop/Marvel LCG/Fusion/marvel-lcg-src' && ~/marvel-work/python/bin/python3.10 launcher_fast.py"
echo.
echo Partie terminee.
pause
exit /b 0

:DEJA_LANCE
echo Une partie tourne deja sur le port 2345.
echo J'ouvre le navigateur dessus plutot que d'en lancer une seconde.
echo.
echo Pour repartir de zero, ferme d'abord le jeu en cours.
start "" "http://127.0.0.1:2345/"
pause
exit /b 0
