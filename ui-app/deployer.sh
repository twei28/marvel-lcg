#!/usr/bin/env bash
# Construit la nouvelle UI et la depose dans le codebase VIVANT du jeu.
#
#   bash ui-app/deployer.sh
#
# A lancer depuis WSL, JAMAIS depuis un script npm : npm passe par cmd.exe,
# ou l'enchainement de commandes POSIX de ce fichier ne fonctionne pas.
set -euo pipefail

# Deduit du fichier lui-meme, jamais ecrit en dur : il existe plusieurs copies de
# ce depot sur le disque (Desktop/"Marvel LCG last try"/ui-app et
# .../Jeu Marvel Champions/ui-app). Un chemin absolu deployait la copie perimee
# tout en laissant croire que le build venait des sources en cours d'edition.
RACINE_APP="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# DEUX installations du jeu, et il faut servir les deux :
#   - Fusion/marvel-lcg-src, a cote de ce depot : c'est celle que lance
#     JOUER-EN-MULTI.bat, donc celle sur laquelle l'utilisateur joue vraiment ;
#   - ~/marvel-work/fusion/marvel-lcg-src : la copie WSL, celle que sert le
#     serveur de developpement du port 2346 et que teste le harnais ui-check.
# Le brief du projet dit que la premiere est perimee. C'est faux, et l'avoir cru
# a fait deployer trois fois de suite dans un jeu auquel personne ne jouait.
JEUX=(
  "$(cd "$RACINE_APP/.." && pwd)/Fusion/marvel-lcg-src"
  "$HOME/marvel-work/fusion/marvel-lcg-src"
)

cd "$RACINE_APP"
npm run build
npm run verifier-sortie

deployer_vers() {
  local JEU="$1"
    mkdir -p "$JEU/public/app" "$JEU/public/css"

  # .game/public est un lien symbolique vers public/ sous launcher_fast.py : la copie
  # est visible immediatement, sans relance du serveur, sans partie perdue.
  rsync -a --delete dist/ "$JEU/public/app/"

  # tokens.css : une seule source, deux destinations.
  # Recopie seulement si le contenu differe : un deploiement qui ne change rien
  # ne doit laisser aucune trace dans l'arborescence du jeu.
  cmp -s styles/tokens.css "$JEU/public/css/tokens.css" \
    || cp styles/tokens.css "$JEU/public/css/tokens.css"

  # Habillage de l'ANCIEN plateau : fond de table et pastilles, en CSS seulement.
  # Il doit etre charge en DERNIER par marvel.html pour gagner a poids egal.
  mkdir -p "$JEU/public/css/marvel"
  cmp -s styles/plateau-habillage.css "$JEU/public/css/marvel/plateau-habillage.css" \
    || cp styles/plateau-habillage.css "$JEU/public/css/marvel/plateau-habillage.css"

  # La balise est posee une seule fois, juste avant </head>. Sans cette garde, un
  # second deploiement en empilerait une deuxieme.
  MARVEL="$JEU/public/marvel.html"
  if [ -f "$MARVEL" ] && ! grep -q 'plateau-habillage\.css' "$MARVEL"; then
    tmp="$(mktemp)"
    sed 's#</head>#    <link rel="stylesheet" href="/public/css/marvel/plateau-habillage.css?v=0">\n</head>#' \
      "$MARVEL" > "$tmp"
    cat "$tmp" > "$MARVEL"
    rm -f "$tmp"
    echo "marvel.html : balise d'habillage ajoutee."
  fi

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
remplacer "$P/scene.html"          'scene-inline\.css' "$P/css/menu/scene-inline.css"
remplacer "$P/prepare.html"        'prepare\.css'  "$P/css/prepare/prepare.css"
remplacer "$P/prepare.html"        'app\.js'       "$P/js/prepare/app.js"

# tokens.css sera reference par les pages anciennes a partir du plan 02-05.
# Ces lignes ne font rien tant que la reference n'existe pas : c'est voulu.
for page in scene.html prepare.html cards.html deck.html replay.html; do
  remplacer "$P/$page" 'tokens\.css' "$P/css/tokens.css"
done

remplacer "$P/marvel.html" 'plateau-habillage\.css' "$P/css/marvel/plateau-habillage.css"

# --- Garde-fou de cascade (plan 02-04) --------------------------------------
# wizard.css a compte jusqu'a 105 declarations !important, qui rendaient toute
# tokenisation impossible : une couche @layer posee au-dessus perdrait contre
# elles. La purge a laisse 2 exceptions, documentees dans le fichier, face a des
# styles poses en ligne par le JavaScript de scene.html.
# Ce compte ne doit pas remonter par accident. S'il doit changer, que ce soit un
# geste conscient : on modifie ce chiffre dans le meme commit, en expliquant
# pourquoi la cascade ne suffisait pas.
IMPORTANTS_ATTENDUS=2
WIZARD="$P/css/menu/wizard.css"
if [ -f "$WIZARD" ]; then
  # Les commentaires du fichier parlent de !important : on les retire avant de compter.
  importants=$(python3 -c "
import re, sys
css = open(sys.argv[1], encoding='utf-8').read()
print(len(re.findall(r'!important', re.sub(r'/\*.*?\*/', '', css, flags=re.S))))
" "$WIZARD")
  if [ "$importants" -ne "$IMPORTANTS_ATTENDUS" ]; then
    echo "ECHEC : wizard.css contient $importants declarations !important, $IMPORTANTS_ATTENDUS attendues." >&2
    echo "La cascade de l'ancienne preparation a ete purgee au plan 02-04. Si une" >&2
    echo "declaration importante est vraiment necessaire, commente-la dans le fichier" >&2
    echo "et mets IMPORTANTS_ATTENDUS a jour ici, dans le meme commit." >&2
    exit 1
  fi
fi

}

deploye=0
for jeu in "${JEUX[@]}"; do
  if [ -d "$jeu/public" ]; then
    echo "--- $jeu"
    deployer_vers "$jeu"
    deploye=$((deploye + 1))
  else
    echo "Ignore (introuvable) : $jeu" >&2
  fi
done

if [ "$deploye" -eq 0 ]; then
  echo "ECHEC : aucune installation du jeu trouvee." >&2
  exit 1
fi

# --- Frontends SERVIS TELS QUELS ---------------------------------------------
# L'assistant de preparation, le salon et le deck-builder ne passent par aucun
# build : ce sont des modules ES servis directement. Ils vivent donc EN DOUBLE,
# un exemplaire par installation, et rien ne les synchronisait — deployer.sh ne
# copiait que dist/.
#
# Ca s'est paye deux fois : le multijoueur a tourne sur un assistant en retard
# de plusieurs correctifs, et il a fallu recopier salon.html, l'assistant et le
# dictionnaire a la main. La source est l'installation WSL, celle qu'on edite.
REFERENCE="$HOME/marvel-work/fusion/marvel-lcg-src"

if [ -d "$REFERENCE/public" ]; then
  for jeu in "${JEUX[@]}"; do
    [ -d "$jeu/public" ] || continue
    [ "$jeu" = "$REFERENCE" ] && continue
    for dossier in js css; do
      [ -d "$REFERENCE/public/$dossier" ] || continue
      # --delete : un fichier supprime a la source doit disparaitre ici aussi,
      # sinon un module mort continuerait d'etre servi. On EXCLUT app/ : c'est
      # dist/, deja traite plus haut, et l'ecraser reviendrait a le vider.
      rsync -a --delete --exclude 'app/' "$REFERENCE/public/$dossier/" "$jeu/public/$dossier/"
    done
    echo "Frontends non compiles synchronises vers $jeu"
  done
fi

echo "Deploye dans $deploye installation(s). Recharge la page dans le navigateur."
