#!/usr/bin/env bash
# Construit la nouvelle UI et la depose dans le codebase VIVANT du jeu.
#
#   bash ui-app/deployer.sh
#
# A lancer depuis WSL, JAMAIS depuis un script npm : npm passe par cmd.exe,
# ou l'enchainement de commandes POSIX de ce fichier ne fonctionne pas.
set -euo pipefail

RACINE_APP="/mnt/c/Users/arnau/Desktop/Marvel LCG last try/ui-app"
JEU="$HOME/marvel-work/fusion/marvel-lcg-src"   # codebase vivant. Fusion/marvel-lcg-src est perime.

cd "$RACINE_APP"
npm run build
node outils/verifier-sortie.mjs

mkdir -p "$JEU/public/app" "$JEU/public/css"

# .game/public est un lien symbolique vers public/ sous launcher_fast.py : la copie
# est visible immediatement, sans relance du serveur, sans partie perdue.
rsync -a --delete dist/ "$JEU/public/app/"

# tokens.css : une seule source, deux destinations.
# Recopie seulement si le contenu differe : un deploiement qui ne change rien
# ne doit laisser aucune trace dans l'arborescence du jeu.
cmp -s styles/tokens.css "$JEU/public/css/tokens.css" \
  || cp styles/tokens.css "$JEU/public/css/tokens.css"

# --- Empreintes de contenu : remplace les ?v=N tenus a la main ---------------
# Le serveur ignore la query string : ?v= n'est qu'une cle de cache navigateur.
# On la recalcule depuis le contenu, a chaque deploiement.
empreinte() { sha256sum "$1" | cut -c1-8; }

remplacer() {           # $1 fichier a editer  $2 nom de fichier reference  $3 fichier source
  local cible="$1" nom="$2" source="$3"
  [ -f "$cible" ] && [ -f "$source" ] || return 0
  # Rien a remplacer = on ne touche pas au fichier. `sed -i` reecrit sa cible
  # meme sans substitution : sans cette garde, chaque deploiement remuerait des
  # pages du jeu qui vivent HORS du depot git, pour rien.
  grep -qE "(${nom})\?v=" "$cible" || return 0
  local tmp; tmp="$(mktemp)"
  sed -E "s|(${nom})\?v=[A-Za-z0-9.]+|\1?v=$(empreinte "$source")|g" "$cible" > "$tmp"
  # Ecriture uniquement si le contenu change, et par redirection (jamais `mv`) :
  # l'inode, les droits et le bit d'execution des fichiers du jeu sont conserves.
  cmp -s "$tmp" "$cible" || cat "$tmp" > "$cible"
  rm -f "$tmp"
}

P="$JEU/public"

# ORDRE OBLIGATOIRE : du plus profond vers le plus superficiel.
# app.js est a la fois une source (pour prepare.html) et une cible (ses imports).
# Le mettre a jour AVANT de calculer son empreinte, sinon prepare.html porterait
# l'empreinte de la version precedente et il faudrait deux deploiements pour
# converger.
remplacer "$P/js/prepare/app.js"   'api\.js'       "$P/js/prepare/api.js"
remplacer "$P/js/prepare/app.js"   'launcher\.js'  "$P/js/prepare/launcher.js"

remplacer "$P/scene.html"          'wizard\.css'   "$P/css/menu/wizard.css"
remplacer "$P/prepare.html"        'prepare\.css'  "$P/css/prepare/prepare.css"
remplacer "$P/prepare.html"        'app\.js'       "$P/js/prepare/app.js"

# tokens.css sera reference par les pages anciennes a partir du plan 02-05.
# Ces lignes ne font rien tant que la reference n'existe pas : c'est voulu.
for page in scene.html prepare.html cards.html deck.html replay.html; do
  remplacer "$P/$page" 'tokens\.css' "$P/css/tokens.css"
done

echo "Deploye. Recharge la page dans le navigateur."
