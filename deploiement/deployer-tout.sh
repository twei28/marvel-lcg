#!/usr/bin/env bash
# Deploie le site normal ET play.<domaine> en une fois, en parallele.
# A lancer seulement apres le « deploie » de l'utilisateur.
#
#   bash deploiement/deployer-tout.sh
#
# 1. construit le plateau (ui-app) une seule fois, pour les deux sites ;
# 2. envoie le site normal (deployer.ps1 -Code, qui redemarre le service) et
#    publie play. (navigateur/publier.py --oui) EN MEME TEMPS ;
# 3. verifie que les deux servent le meme plateau que le poste.
# play. ne rejoue son controle d'equivalence (20 parties) que si le moteur a
# change depuis le dernier controle reussi.
set -uo pipefail
cd "$(dirname "$0")/.."
RACINE="$(pwd)"
JOURNAUX="$(mktemp -d)"
CLE_WIN="$(wslpath -w "$RACINE/deploiement/cle_narwhal")"
HOTE=root@178.105.177.39

# LE JOURNAL DES NOUVEAUTES DOIT SUIVRE LE CODE (08/10/2026). Il etait reste
# au 05/10 pendant six deploiements : les joueurs ne savaient pas ce qui avait
# change. Le deploiement s'arrete si une fonctionnalite ou une correction a ete
# commitee APRES la derniere entree de `nouveautes.js`. Pour passer outre (rien
# a annoncer aux joueurs) : NOUVEAUTES_A_JOUR=1 bash deploiement/deployer-tout.sh
NOUVEAUTES="Fusion/marvel-lcg-src/public/js/prepare/nouveautes.js"
derniere_entree=$(grep -oE 'date: "[0-9-]+"' "$NOUVEAUTES" | cut -d'"' -f2 | sort -r | head -1)
# Les commits « feat(admin) » / « fix(admin) » ne concernent que l'administrateur : rien a annoncer.
dernier_changement=$(git log -E --grep='^(feat|fix)' --format='%ad %s' --date=short -- ui-app Fusion/marvel-lcg-src/src Fusion/marvel-lcg-src/public Fusion/marvel-lcg-src/data site \
  | grep -vE '^[0-9-]+ (feat|fix)\(admin\)' | head -1 | cut -d' ' -f1)
if [[ "$dernier_changement" > "$derniere_entree" && "${NOUVEAUTES_A_JOUR:-}" != "1" ]]; then
  echo "ARRET : le journal des nouveautes s'arrete au $derniere_entree, le code a change le $dernier_changement."
  echo "        Ajoute les entrees (fr + en) dans $NOUVEAUTES, ou relance avec NOUVEAUTES_A_JOUR=1."
  exit 1
fi
echo "   nouveautes a jour (derniere entree $derniere_entree)"

echo "== Plateau"
bash ui-app/deployer.sh > "$JOURNAUX/plateau.log" 2>&1 || { tail -20 "$JOURNAUX/plateau.log"; exit 1; }
tail -1 "$JOURNAUX/plateau.log"

echo "== Envoi des deux sites en parallele (journaux : $JOURNAUX)"
powershell.exe -ExecutionPolicy Bypass -File "$(wslpath -w "$RACINE/deploiement/deployer.ps1")" -Code \
  > "$JOURNAUX/normal.log" 2>&1 &
normal=$!
python3 navigateur/publier.py --oui > "$JOURNAUX/play.log" 2>&1 &
play=$!
# La sauvegarde du code, fabriquee pendant les envois (sauvegarde-code.sh).
bash deploiement/sauvegarde-code.sh "$JOURNAUX" > "$JOURNAUX/sauvegarde.log" 2>&1 &
sauvegarde=$!
wait $normal; r_normal=$?
echo "   site normal : $([ $r_normal -eq 0 ] && echo termine || echo "ECHEC ($r_normal)")"
wait $play; r_play=$?
echo "   play.       : $([ $r_play -eq 0 ] && echo termine || echo "ECHEC ($r_play)")"
grep -E "identiques,|controle saute|ARRET" "$JOURNAUX/play.log" | sed 's/^/   /'

# Les sons de play. ne viennent pas du paquet publie mais de
# /opt/narwhal-play-scans/originaux/sounds (Caddy, /_son/) : sans cette copie,
# un son ajoute au depot marche sur le site normal et manque sur play.
if [ $r_normal -eq 0 ]; then
  ssh.exe -i "$CLE_WIN" "$HOTE" "cp -u /opt/narwhal/Fusion/marvel-lcg-src/assets/sounds/*.wav /opt/narwhal/Fusion/marvel-lcg-src/assets/sounds/*.mp3 /opt/narwhal-play-scans/originaux/sounds/; chown 1000:1000 /opt/narwhal-play-scans/originaux/sounds/*; ls /opt/narwhal-play-scans/originaux/sounds | wc -l" \
    | sed 's/^/   sons de play. : /'
fi

echo "== Sauvegarde du code"
if wait $sauvegarde; then
  ZIP="$(tail -1 "$JOURNAUX/sauvegarde.log")"
  NOM_ZIP="$(basename "$ZIP")"
  cp "$ZIP" "$RACINE/deploiement/_a_supprimer/$NOM_ZIP"
  if scp.exe -q -i "$CLE_WIN" "$(wslpath -w "$RACINE/deploiement/_a_supprimer/$NOM_ZIP")" "$HOTE:/tmp/$NOM_ZIP"; then
    ssh.exe -i "$CLE_WIN" "$HOTE" "set -e; D=/opt/narwhal/sauvegardes-code; mkdir -p \$D; mv /tmp/$NOM_ZIP \$D/; ls -1 \$D/code-*.zip | sort -r | tail -n +6 | xargs -r rm -f; chown -R narwhal:narwhal \$D; ls \$D | wc -l" \
      | sed 's/^/   sauvegardes sur le serveur : /'
    echo "   $NOM_ZIP envoye ($(du -h "$ZIP" | cut -f1))"
  else
    echo "   ⚠ envoi de la sauvegarde en echec (le deploiement, lui, est fait)"
  fi
  rm -f "$RACINE/deploiement/_a_supprimer/$NOM_ZIP"
else
  echo "   ⚠ sauvegarde du code en echec, voir $JOURNAUX/sauvegarde.log"
fi

echo "== Verification"
local_js=$(md5sum Fusion/marvel-lcg-src/public/app/assets/board-*.js | cut -c1-32)
distant=$(ssh.exe -i "$CLE_WIN" "$HOTE" \
  "md5sum /opt/narwhal/Fusion/marvel-lcg-src/public/app/assets/board-*.js | cut -c1-32; systemctl is-active narwhal; ls /opt/narwhal-play/app/assets/ | grep -E '^board-.*\.js$'")
echo "$distant" | sed 's/^/   /'
nom_local=$(basename Fusion/marvel-lcg-src/public/app/assets/board-*.js)
echo "$distant" | grep -q "$local_js" && echo "   site normal : meme plateau que le poste ($nom_local)" || echo "   ⚠ site normal : plateau DIFFERENT du poste"
echo "$distant" | grep -q "$nom_local" && echo "   play.       : meme plateau que le poste" || echo "   ⚠ play. : plateau DIFFERENT du poste"
for url in https://narwhalchampions.com/ https://play.narwhalchampions.com/navigateur.html; do
  echo "   $url -> $(curl -s -o /dev/null -w '%{http_code}' "$url")"
done
[ $r_normal -eq 0 ] && [ $r_play -eq 0 ]
