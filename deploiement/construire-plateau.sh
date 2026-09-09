#!/usr/bin/env bash
# Construit le plateau (ui-app/deployer.sh) depuis WSL, pour DEPLOYER.bat.
#
# Pourquoi un fichier et pas une ligne dans le .bat : cmd.exe, wsl.exe et bash
# se passent la commande en se disputant les guillemets, et un chemin avec une
# espace (« Marvel LCG ») n'y survit pas (constate le 09/09/2026). Un script
# a UN argument, son propre chemin, passe partout.
set -euo pipefail
cd "$(dirname "$0")/.."
exec bash ui-app/deployer.sh
