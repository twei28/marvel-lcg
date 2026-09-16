#!/usr/bin/env bash
# =============================================================================
#  Le filet memoire du serveur : zram, puis un swap disque.
#
#      sudo bash memoire-serveur.sh            (pose ou met a jour)
#      sudo bash memoire-serveur.sh --etat     (montre, ne touche a rien)
#
#  ⚠ POURQUOI. Mesure du 16/09/2026 : la machine a 3,8 Go, AUCUN swap, et une
#  table de jeu coute 221 Mo. Sans filet, une memoire pleine ne ralentit pas :
#  le noyau tue un processus au hasard, sans prevenir. Ce serait une partie en
#  cours qui disparait sans explication.
#
#  ⚠ DEUX ETAGES, ET L'ORDRE COMPTE.
#    1. zram : on COMPRIME la memoire inutilisee, sans toucher au disque. Les
#       objets Python se compriment bien. Priorite HAUTE, c'est le premier
#       recours et il est rapide.
#    2. un fichier d'echange de 4 Go sur le disque (28 Go y sont libres) :
#       priorite BASSE, dernier recours pour les pages froides d'une table que
#       personne ne touche.
#
#  ⚠ IDEMPOTENT : relancable sans rien casser. Il ne recree pas ce qui est deja
#  en place, et n'ecrit dans /etc/fstab qu'une seule fois.
# =============================================================================
set -e

TAILLE_SWAP="${TAILLE_SWAP:-4G}"
FICHIER_SWAP="${FICHIER_SWAP:-/swapfile}"
# Moitie de la RAM pour zram : au-dela, on comprime plus qu'on ne garde de
# place pour travailler.
TAILLE_ZRAM="${TAILLE_ZRAM:-50}"      # en pourcentage de la RAM

etat() {
  echo "=== memoire ==="
  free -m | head -2
  echo "=== ce qui sert d'echange ==="
  swapon --show 2>/dev/null || echo "  (aucun)"
  echo "=== reglages ==="
  echo "  vm.swappiness = $(cat /proc/sys/vm/swappiness)"
  echo "  vm.vfs_cache_pressure = $(cat /proc/sys/vm/vfs_cache_pressure)"
}

if [ "${1:-}" = "--etat" ]; then
  etat
  exit 0
fi

# ⚠ LE MODE QUE L'UNIT SYSTEMD UTILISE. Au demarrage, le fichier d'echange est
# remonte par /etc/fstab et les reglages par /etc/sysctl.d : il ne reste que
# zram a refaire, car il vit en memoire et disparait a l'extinction.
ZRAM_SEULEMENT=0
[ "${1:-}" = "--zram" ] && ZRAM_SEULEMENT=1

[ "$(id -u)" = "0" ] || { echo "A lancer en root." >&2; exit 1; }

# --- 1. zram ------------------------------------------------------------------
# `systemd-zram-generator` n'est pas installe partout ; `zramctl` vient
# d'util-linux, donc il est deja la. On pose une unit qui refait le montage au
# demarrage, sans dependre d'un paquet a installer.
if ! swapon --show=NAME --noheadings 2>/dev/null | grep -q zram; then
  modprobe zram num_devices=1 2>/dev/null || true
  if [ -e /dev/zram0 ]; then
    ram_ko=$(awk '/MemTotal/ {print $2}' /proc/meminfo)
    taille_ko=$(( ram_ko * TAILLE_ZRAM / 100 ))
    zramctl --reset /dev/zram0 2>/dev/null || true
    zramctl --find --size "${taille_ko}KiB" --algorithm zstd >/dev/null 2>&1 \
      || zramctl /dev/zram0 --size "${taille_ko}KiB" >/dev/null
    mkswap /dev/zram0 >/dev/null
    # Priorite HAUTE : on comprime avant d'ecrire sur le disque.
    swapon --priority 100 /dev/zram0
    echo "zram pose : $(( taille_ko / 1024 )) Mo, priorite 100"
  else
    echo "⚠ zram indisponible sur ce noyau, on continue sans." >&2
  fi
else
  echo "zram deja en place."
fi

# L'unit appelle ce script : il doit donc exister a demeure quelque part.
install -m 755 "$0" /usr/local/bin/narwhal-memoire

# ⚠ L'UNIT N'EXISTE QUE SI ZRAM EXISTE. Une unit activee qui ne peut rien faire
# est un piege : elle apparait dans `systemctl` comme un service du jeu, et la
# prochaine personne qui lit cette liste se demandera pourquoi elle ne tourne
# pas. Sur ce serveur, le module zram est absent du noyau et elle n'est donc
# pas posee.
if [ -e /dev/zram0 ]; then
cat > /etc/systemd/system/narwhal-zram.service <<'UNIT'
[Unit]
Description=NarwhalChampions — zram (compression de la memoire)
DefaultDependencies=no
Before=swap.target
After=systemd-modules-load.service

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/usr/local/bin/narwhal-memoire --zram
ExecStop=/bin/sh -c '/sbin/swapoff /dev/zram0 || true'

[Install]
WantedBy=swap.target
UNIT
  systemctl daemon-reload
  systemctl enable narwhal-zram.service >/dev/null 2>&1 || true
else
  # Pose par une version precedente de ce script, alors que zram n'existait pas.
  if [ -f /etc/systemd/system/narwhal-zram.service ]; then
    systemctl disable narwhal-zram.service >/dev/null 2>&1 || true
    rm -f /etc/systemd/system/narwhal-zram.service
    systemctl daemon-reload
    echo "unit zram retiree : le module n'existe pas sur ce noyau."
  fi
fi

# --- 2. Le fichier d'echange sur disque ---------------------------------------
if [ "$ZRAM_SEULEMENT" = "1" ]; then
  exit 0
fi

if ! swapon --show=NAME --noheadings 2>/dev/null | grep -q "^$FICHIER_SWAP$"; then
  if [ ! -f "$FICHIER_SWAP" ]; then
    fallocate -l "$TAILLE_SWAP" "$FICHIER_SWAP" 2>/dev/null \
      || dd if=/dev/zero of="$FICHIER_SWAP" bs=1M count=4096 status=none
    chmod 600 "$FICHIER_SWAP"
    mkswap "$FICHIER_SWAP" >/dev/null
  fi
  # Priorite BASSE : dernier recours, apres zram.
  swapon --priority 10 "$FICHIER_SWAP"
  echo "fichier d'echange pose : $FICHIER_SWAP ($TAILLE_SWAP), priorite 10"
else
  echo "fichier d'echange deja en place."
fi

if ! grep -q "^$FICHIER_SWAP " /etc/fstab 2>/dev/null; then
  echo "$FICHIER_SWAP none swap sw,pri=10 0 0" >> /etc/fstab
  echo "fstab : ligne ajoutee."
fi

# --- 3. Les reglages du noyau -------------------------------------------------
# ⚠ `swappiness` DEPEND DE CE QUI EST REELLEMENT LA, et se tromper coute cher.
#   - avec zram, « echanger » veut dire « comprimer », en memoire, vite : 100
#     est le bon reglage, le defaut de 60 est pense pour un disque lent ;
#   - SANS zram, 100 revient a ecrire agressivement sur le disque et a ralentir
#     tout le monde pour economiser une memoire dont on a la place. On revient
#     alors au defaut, et le fichier d'echange ne sert plus que de filet.
#
# Mesure du 16/09/2026 sur ce serveur : le module zram est ABSENT du noyau
# 5.15.0-190-generic (Ubuntu le range dans `linux-modules-extra`, non installe).
# D'ou ce choix automatique plutot qu'une valeur ecrite en dur.
if swapon --show=NAME --noheadings 2>/dev/null | grep -q zram; then
  SWAPPINESS=100
  POURQUOI="zram present : comprimer plutot qu'ecrire"
else
  SWAPPINESS=60
  POURQUOI="pas de zram : le disque n'est qu'un filet, on ne l'use pas"
fi
cat > /etc/sysctl.d/99-narwhal-memoire.conf <<SYSCTL
# NarwhalChampions, pose par memoire-serveur.sh.
# $POURQUOI
vm.swappiness = $SWAPPINESS
vm.vfs_cache_pressure = 50
SYSCTL
sysctl -q --system

echo
etat
