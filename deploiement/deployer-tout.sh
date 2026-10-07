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

echo "== Plateau"
bash ui-app/deployer.sh > "$JOURNAUX/plateau.log" 2>&1 || { tail -20 "$JOURNAUX/plateau.log"; exit 1; }
tail -1 "$JOURNAUX/plateau.log"

echo "== Envoi des deux sites en parallele (journaux : $JOURNAUX)"
powershell.exe -ExecutionPolicy Bypass -File "$(wslpath -w "$RACINE/deploiement/deployer.ps1")" -Code \
  > "$JOURNAUX/normal.log" 2>&1 &
normal=$!
python3 navigateur/publier.py --oui > "$JOURNAUX/play.log" 2>&1 &
play=$!
wait $normal; r_normal=$?
echo "   site normal : $([ $r_normal -eq 0 ] && echo termine || echo "ECHEC ($r_normal)")"
wait $play; r_play=$?
echo "   play.       : $([ $r_play -eq 0 ] && echo termine || echo "ECHEC ($r_play)")"
grep -E "identiques,|controle saute|ARRET" "$JOURNAUX/play.log" | sed 's/^/   /'

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
