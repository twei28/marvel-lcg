#!/usr/bin/env bash
# Fabrique la sauvegarde du code (08/10/2026) : un zip avec tout le projet SANS
# les images, et tout l'historique Git sans les fichiers de plus de 2 Mo.
#
#   bash deploiement/sauvegarde-code.sh <dossier de sortie>   -> affiche le chemin du zip
#
# Appele par deployer-tout.sh, qui l'envoie sur le serveur (les 5 derniers y
# sont gardes, telechargeables par l'administrateur sur /admin/sauvegardes).
# Seul ce qui est COMMITE part : le travail en cours non commite n'y est pas.
set -euo pipefail
cd "$(dirname "$0")/.."
RACINE="$(pwd)"
SORTIE="$1"
TRAVAIL="$(mktemp -d)"
trap 'rm -rf "$TRAVAIL"' EXIT

HASH="$(git rev-parse --short HEAD)"
BRANCHE="$(git rev-parse --abbrev-ref HEAD)"
NOM="code-$(date +%Y%m%d-%H%M)-$HASH.zip"

# L'historique, toutes branches, sans les gros fichiers (images, archives).
git clone -q --mirror "$RACINE" "$TRAVAIL/depot.git"
git -C "$TRAVAIL/depot.git" filter-repo --force --quiet --strip-blobs-bigger-than 2M >/dev/null 2>&1
git -C "$TRAVAIL/depot.git" bundle create "$TRAVAIL/historique.bundle" --all >/dev/null 2>&1

# Le code tel quel, branche courante, pour qui n'utilise pas Git.
mkdir -p "$TRAVAIL/code"
git archive --format=tar HEAD | tar -x -C "$TRAVAIL/code"

cat > "$TRAVAIL/LISEZ-MOI.txt" <<EOF
Sauvegarde du code de Marvel Champions (Narwhal Champions)
Faite le $(date '+%d/%m/%Y a %H:%M'), branche $BRANCHE, version $HASH.

Contenu :
  code/               le projet tel qu'il etait, SANS les images (scans, vignettes).
  historique.bundle   tout l'historique Git, toutes les branches, sans les
                      fichiers de plus de 2 Mo.

Repartir de cette sauvegarde (avec Git installe) :
  git clone historique.bundle "Marvel LCG"
  cd "Marvel LCG"
  git checkout $BRANCHE

Les images (scans, vignettes, HD, sons, documents, environ 2,5 Go) ne sont
pas dans ce zip. Pour les recuperer :
  1. sur le site, connecte avec le compte administrateur, ouvrir
     https://narwhalchampions.com/admin/sauvegardes et cliquer sur « Toutes les
     images » : un fichier images-AAAAMMJJ.tar se telecharge ;
  2. l'extraire dans le dossier Fusion/marvel-lcg-src/ du projet restaure
     (il contient le dossier assets/), par exemple :
       tar -xf images-AAAAMMJJ.tar -C "Marvel LCG/Fusion/marvel-lcg-src"
Le programme lit ses images dans Fusion/marvel-lcg-src/assets/ : rien d'autre
a relier.
EOF

python3 - "$TRAVAIL" "$SORTIE/$NOM" <<'PY'
import os, sys, zipfile
source, cible = sys.argv[1], sys.argv[2]
with zipfile.ZipFile(cible, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for dossier, sous, fichiers in os.walk(source):
        sous[:] = [d for d in sous if d != "depot.git"]
        for f in fichiers:
            chemin = os.path.join(dossier, f)
            z.write(chemin, os.path.relpath(chemin, source))
PY
echo "$SORTIE/$NOM"
