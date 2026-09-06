#!/usr/bin/env bash
# ==============================================================================
# NarwhalChampions — installation d'un VPS neuf (Ubuntu 22.04 LTS, x86_64)
#
#   scp install-serveur.sh root@IP:/root/
#   ssh root@IP "DOMAINE=narwhalchampions.com CF_API_TOKEN=xxx EMAIL_ACME=vous@narwhalchampions.com bash install-serveur.sh"
#
# Ubuntu 22.04 est choisi parce qu'il fournit python3.10 en paquet natif :
# ni PPA, ni compilation, ni pyenv.
# ==============================================================================
set -euo pipefail

DOMAINE="${DOMAINE:?DOMAINE manquant (ex. narwhalchampions.com)}"
CF_API_TOKEN="${CF_API_TOKEN:?CF_API_TOKEN manquant (jeton Cloudflare, droit Zone:DNS:Edit)}"
EMAIL_ACME="${EMAIL_ACME:?EMAIL_ACME manquant (adresse pour Lets Encrypt)}"
UTILISATEUR="${UTILISATEUR:-narwhal}"
RACINE="${RACINE:-/opt/narwhal}"

echo "==> 1/8  Base système"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get -y -qq upgrade
# sqlite3 : CLI necessaire a sauvegarde.sh (".backup", instantane coherent
# de narwhal.db malgre le mode WAL).
apt-get -y -qq install \
  rsync ufw curl ca-certificates gnupg git unzip \
  imagemagick jq sqlite3 \
  python3.10 python3.10-venv python3.10-dev python3-pip \
  debian-keyring debian-archive-keyring apt-transport-https
python3.10 --version

echo "==> 2/8  Utilisateur applicatif et arborescence"
if ! id -u "$UTILISATEUR" >/dev/null 2>&1; then
  useradd --system --create-home --home-dir "$RACINE" --shell /bin/bash "$UTILISATEUR"
fi
mkdir -p "$RACINE"/{Fusion/marvel-lcg-src,site,sauvegardes,journaux}
chown -R "$UTILISATEUR:$UTILISATEUR" "$RACINE"
mkdir -p /var/backups/narwhal /var/log/caddy
chown "$UTILISATEUR:$UTILISATEUR" /var/backups/narwhal

echo "==> 3/8  Clé SSH du déploiement"
# La clé publique de votre poste doit pouvoir écrire dans $RACINE.
install -d -m 700 -o "$UTILISATEUR" -g "$UTILISATEUR" "$RACINE/.ssh"
if [ -f /root/.ssh/authorized_keys ]; then
  install -m 600 -o "$UTILISATEUR" -g "$UTILISATEUR" \
    /root/.ssh/authorized_keys "$RACINE/.ssh/authorized_keys"
fi

echo "==> 4/8  Caddy avec le module DNS Cloudflare"
# Le paquet officiel n'embarque pas caddy-dns/cloudflare : on installe le paquet
# (pour l'unité systemd et l'utilisateur caddy), puis on remplace le binaire par
# une version construite avec le module.
if ! command -v caddy >/dev/null 2>&1; then
  curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' \
    | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
  curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' \
    > /etc/apt/sources.list.d/caddy-stable.list
  apt-get update -qq
  apt-get -y -qq install caddy
fi
if ! caddy list-modules 2>/dev/null | grep -q '^dns.providers.cloudflare$'; then
  curl -fsSL -o /tmp/caddy-cf \
    "https://caddyserver.com/api/download?os=linux&arch=amd64&p=github.com%2Fcaddy-dns%2Fcloudflare"
  chmod +x /tmp/caddy-cf
  /tmp/caddy-cf list-modules | grep -q '^dns.providers.cloudflare$'
  systemctl stop caddy 2>/dev/null || true
  mv /tmp/caddy-cf /usr/bin/caddy
  # apt ne doit pas réécraser le binaire au prochain upgrade
  apt-mark hold caddy
fi
caddy list-modules | grep '^dns.providers.cloudflare$'

echo "==> 5/8  Variables de Caddy et Caddyfile"
umask 077
cat > /etc/caddy/cloudflare.env <<ENV
DOMAINE=$DOMAINE
EMAIL_ACME=$EMAIL_ACME
CF_API_TOKEN=$CF_API_TOKEN
ENV
chmod 640 /etc/caddy/cloudflare.env
chown root:caddy /etc/caddy/cloudflare.env
umask 022
mkdir -p /etc/systemd/system/caddy.service.d
cat > /etc/systemd/system/caddy.service.d/cloudflare.conf <<'ENV'
[Service]
EnvironmentFile=/etc/caddy/cloudflare.env
ENV
install -m 644 Caddyfile /etc/caddy/Caddyfile
chown -R caddy:caddy /var/log/caddy
# Contrôle de syntaxe avant tout démarrage : les variables sont lues ici, donc
# une faute de frappe dans le Caddyfile ou un jeton absent se voit tout de suite.
set -a; . /etc/caddy/cloudflare.env; set +a
caddy validate --adapter caddyfile --config /etc/caddy/Caddyfile

echo "==> 6/8  Services systemd"
install -m 644 narwhal.service            /etc/systemd/system/narwhal.service
install -m 644 narwhal-sauvegarde.service /etc/systemd/system/narwhal-sauvegarde.service
install -m 644 narwhal-sauvegarde.timer   /etc/systemd/system/narwhal-sauvegarde.timer
install -m 644 narwhal-purge.service      /etc/systemd/system/narwhal-purge.service
install -m 644 narwhal-purge.timer        /etc/systemd/system/narwhal-purge.timer
install -m 755 sauvegarde.sh /usr/local/bin/narwhal-sauvegarde
install -m 755 purge.sh      /usr/local/bin/narwhal-purge
sed -i "s|@RACINE@|$RACINE|g; s|@UTILISATEUR@|$UTILISATEUR|g; s|@DOMAINE@|$DOMAINE|g" \
  /etc/systemd/system/narwhal.service \
  /etc/systemd/system/narwhal-sauvegarde.service \
  /etc/systemd/system/narwhal-purge.service \
  /usr/local/bin/narwhal-sauvegarde \
  /usr/local/bin/narwhal-purge

cat > /etc/sudoers.d/narwhal <<SUDO
# L'utilisateur applicatif redémarre son propre service et déclenche sa
# sauvegarde depuis le script de déploiement, sans mot de passe et sans rien
# d'autre.
$UTILISATEUR ALL=(root) NOPASSWD: /usr/bin/systemctl restart narwhal, /usr/bin/systemctl stop narwhal, /usr/bin/systemctl start narwhal, /usr/local/bin/narwhal-sauvegarde
SUDO
chmod 440 /etc/sudoers.d/narwhal
visudo -c -q

echo "==> 7/8  Pare-feu : 22, 80, 443 et rien d'autre"
ufw --force reset >/dev/null
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp   comment 'SSH'
ufw allow 80/tcp   comment 'HTTP (redirection + ACME)'
ufw allow 443/tcp  comment 'HTTPS'
ufw --force enable
ufw status verbose
# 8080 et 2351-2370 ne sont jamais ouverts : Caddy les joint en 127.0.0.1,
# personne d'autre ne les joint du tout.

echo "==> 8/8  Activation"
systemctl daemon-reload
systemctl enable --now caddy
systemctl enable narwhal-sauvegarde.timer narwhal-purge.timer
systemctl start  narwhal-sauvegarde.timer narwhal-purge.timer
# narwhal.service n'est pas démarré ici : le code n'est pas encore là.
systemctl enable narwhal

cat <<MSG

--------------------------------------------------------------------------
Serveur prêt. Le code du jeu n'est pas encore installé.

Depuis votre poste :
    ./deployer.sh            (pousse le code + les images, puis démarre)

Vérifications utiles :
    systemctl status caddy
    journalctl -u caddy -n 50
--------------------------------------------------------------------------
MSG
