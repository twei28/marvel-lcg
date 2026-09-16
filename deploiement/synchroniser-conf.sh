#!/usr/bin/env bash
# =============================================================================
#  Aligne les scripts et la configuration du serveur sur le depot.
#
#      bash synchroniser-conf.sh <racine> <utilisateur> <domaine>
#
#  Appele par `deployer.ps1` a chaque deploiement, depuis /tmp/narwhal-conf.
#
#  ⚠ POURQUOI CE FICHIER EXISTE, ET PAS UNE CHAINE DANS LE .PS1. Le bash etait
#  d'abord ecrit dans une here-string PowerShell. Les guillemets doubles n'ont
#  pas survecu au passage a `ssh.exe` : le `sed` de substitution est arrive
#  sans ses guillemets, ses « | » sont devenus des pipes, et le deploiement
#  s'est arrete sur « /opt/narwhal: Is a directory ». Un fichier envoye puis
#  execute n'a aucun de ces problemes, et il se relit.
#
#  ⚠ DEUX LISTES, ET LA DISTINCTION EST VITALE (mesure du 16/09/2026).
#  Trois fichiers du serveur avaient derive, et DEUX dans le bon sens :
#    - /etc/caddy/Caddyfile importe deux AUTRES sites (karaoke, publicverse) :
#      l'ecraser les aurait coupes ;
#    - narwhal.service porte `Environment=INSCRIPTION_LIBRE=0`, pose a la main :
#      l'ecraser aurait rouvert l'inscription a n'importe qui.
#  Ces deux-la sont SURVEILLES : on montre l'ecart, on ne touche a rien.
# =============================================================================
set -e

RACINE="${1:?racine attendue}"
UTILISATEUR="${2:?utilisateur attendu}"
DOMAINE="${3:?domaine attendu}"
cd "$(dirname "$0")"

# Les memes substitutions que `install-serveur.sh`, sur les memes fichiers.
sed -i "s|@RACINE@|$RACINE|g; s|@UTILISATEUR@|$UTILISATEUR|g; s|@DOMAINE@|$DOMAINE|g" \
  sauvegarde.sh purge.sh narwhal.service narwhal-sauvegarde.service narwhal-purge.service

recharger=0

# --- Ce qui appartient ENTIEREMENT au depot : on synchronise ------------------
poser() {            # $1 source  $2 cible  $3 droits  $4 "unit" si systemd
  if cmp -s "$1" "$2" 2>/dev/null; then
    echo "   a jour     : $2"
    return 0
  fi
  # Une unit invalide n'est PAS posee : une erreur de frappe ici empecherait le
  # service de redemarrer, et le deploiement est justement en train d'y aller.
  if [ "$4" = "unit" ] && ! systemd-analyze verify "$1" >/dev/null 2>&1; then
    echo "   REFUSE     : $2 ne passe pas systemd-analyze verify, rien n'est pose" >&2
    return 0
  fi
  avant="(absent)"
  [ -f "$2" ] && avant="$(date -r "$2" +%d/%m)"
  install -m "$3" "$1" "$2"
  echo "   MIS A JOUR : $2 (l'ancien datait du $avant)"
  [ "$4" = "unit" ] && recharger=1
  return 0
}

poser sauvegarde.sh              /usr/local/bin/narwhal-sauvegarde              755
poser purge.sh                   /usr/local/bin/narwhal-purge                   755
poser narwhal-sauvegarde.service /etc/systemd/system/narwhal-sauvegarde.service 644 unit
poser narwhal-purge.service      /etc/systemd/system/narwhal-purge.service      644 unit
poser narwhal-sauvegarde.timer   /etc/systemd/system/narwhal-sauvegarde.timer   644 unit
poser narwhal-purge.timer        /etc/systemd/system/narwhal-purge.timer        644 unit

if [ "$recharger" = "1" ]; then
  systemctl daemon-reload
  echo "   systemd recharge"
fi

# --- Ce qui porte des reglages du serveur : on REGARDE, on ne touche pas ------
surveiller() {       # $1 source  $2 cible
  if cmp -s "$1" "$2" 2>/dev/null; then
    echo "   identique  : $2"
    return 0
  fi
  echo "   DIFFERENT (non touche) : $2"
  diff "$1" "$2" | head -12 | sed 's/^/       /' || true
  return 0
}

surveiller narwhal.service /etc/systemd/system/narwhal.service
surveiller Caddyfile       /etc/caddy/Caddyfile
