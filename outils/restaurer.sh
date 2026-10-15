#!/usr/bin/env bash
# Restaure le projet sur une machine vide (15/10/2026).
#
#   bash restaurer.sh [dossier]          (defaut : ./Marvel LCG)
#
# Trois etages, chacun optionnel selon ce qui est fourni :
#   1. le CODE      : git clone du depot GITHUB prive (necessite `gh auth login`
#                     ou un acces git deja configure).
#   2. les IMAGES   : tar fabrique par le site, https://<domaine>/admin/images.
#                     Reserve a l'administrateur : exporter NC_SESSION avec la
#                     valeur du cookie `nc_session` (navigateur connecte en
#                     admin > outils de developpement > cookies).
#   3. le RESTE     : paquets-cartes/, medias/, "A creer"/, captures/ et les
#                     images jamais deployees, gardes sur le serveur dans
#                     /var/backups/narwhal/poste/. Necessite la cle SSH
#                     (deploiement/cle_narwhal, a recuperer sur la cle USB) :
#                     exporter CLE_SSH=/chemin/vers/cle_narwhal.
#
# Variables : DEPOT (defaut twei28/marvel-lcg), BRANCHE (defaut
# sauvegarde-cle-usb-2026-10-14), DOMAINE (defaut narwhalchampions.com),
# SERVEUR (defaut root@178.105.177.39).
# Rien n'est jamais supprime : le script ajoute, il n'efface pas.
set -euo pipefail

DOSSIER="${1:-Marvel LCG}"
DEPOT="${DEPOT:-twei28/marvel-lcg}"
BRANCHE="${BRANCHE:-sauvegarde-cle-usb-2026-10-14}"
DOMAINE="${DOMAINE:-narwhalchampions.com}"
SERVEUR="${SERVEUR:-root@178.105.177.39}"

etape() { printf '\n=== %s\n' "$*"; }

etape "1/3 Code (GitHub, depot prive $DEPOT)"
if [ -d "$DOSSIER/.git" ]; then
  echo "Deja present, on met a jour."
  git -C "$DOSSIER" fetch --all --prune
else
  if command -v gh >/dev/null 2>&1; then
    gh repo clone "$DEPOT" "$DOSSIER" -- --branch "$BRANCHE"
  else
    git clone --branch "$BRANCHE" "https://github.com/$DEPOT.git" "$DOSSIER"
  fi
fi

etape "2/3 Images (HTTPS, https://$DOMAINE/admin/images)"
if [ -n "${NC_SESSION:-}" ]; then
  TAR="$(mktemp --suffix=.tar)"
  trap 'rm -f "$TAR"' EXIT
  curl -fL --retry 3 -H "Cookie: nc_session=$NC_SESSION" \
       -o "$TAR" "https://$DOMAINE/admin/images"
  # On n'ecrase pas ce qui existe deja.
  tar -xf "$TAR" -C "$DOSSIER/Fusion/marvel-lcg-src" --skip-old-files
  echo "Images extraites dans $DOSSIER/Fusion/marvel-lcg-src/assets/"
else
  echo "NC_SESSION absent : etape sautee (voir l'en-tete de ce script)."
fi

etape "3/3 Le reste (serveur, /var/backups/narwhal/poste/)"
if [ -n "${CLE_SSH:-}" ] && [ -f "${CLE_SSH}" ]; then
  chmod 600 "$CLE_SSH" 2>/dev/null || true
  SSH="ssh -i $CLE_SSH"
  for d in paquets-cartes medias "A créer" captures; do
    rsync -a --ignore-existing -e "$SSH" "$SERVEUR:/var/backups/narwhal/poste/$d" "$DOSSIER/"
  done
  # Images jamais deployees : a ajouter dans assets/ sans ecraser.
  rsync -a --ignore-existing -e "$SSH" \
        "$SERVEUR:/var/backups/narwhal/poste/assets-locaux/" "$DOSSIER/Fusion/marvel-lcg-src/assets/"
else
  echo "CLE_SSH absent : etape sautee (voir l'en-tete de ce script)."
fi

etape "Verification"
A="$DOSSIER/Fusion/marvel-lcg-src/assets"
for sous in pics pics-fr pics-hd vignettes sounds textures docs; do
  printf '%-12s %s fichiers\n' "$sous" "$( [ -d "$A/$sous" ] && find "$A/$sous" -type f | wc -l || echo 0 )"
done
echo
echo "Attendu (15/10/2026) : pics ~7000, pics-fr 4563, pics-hd ~600, vignettes ~10900."
