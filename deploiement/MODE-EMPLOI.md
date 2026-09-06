# NarwhalChampions — mode d'emploi

Tout se pilote depuis ce dossier (`Bureau\Marvel LCG\deploiement`).

| | |
|---|---|
| Domaine | narwhalchampions.com (Cloudflare, renouvellement auto) |
| Serveur | Hetzner CX23, Nuremberg, Ubuntu 22.04 |
| IP | 178.105.177.39 |
| Coût | ~9,50 €/an + 7,25 €/mois TTC |

---

## Déjà fait

- Domaine acheté, zone DNS créée.
- Entrées DNS : `narwhalchampions.com` et `*.narwhalchampions.com` vers l'IP,
  toutes deux en **DNS only** (nuage gris) — ne les passez jamais en orange,
  le WebSocket des parties passerait par un intermédiaire.
- Jeton API Cloudflare créé (portée : DNS de cette zone uniquement), inscrit
  dans `installer-serveur.ps1`.
- Serveur créé avec la clé SSH `cle_narwhal` de ce dossier.

## À faire, dans l'ordre

### 1. Installer le serveur — une seule fois

Clic droit sur **`installer-serveur.ps1`** → *Exécuter avec PowerShell*.
(Ou : `powershell -ExecutionPolicy Bypass -File .\installer-serveur.ps1`)

Compter cinq à dix minutes : Python 3.10, Caddy avec le module DNS Cloudflare,
le pare-feu (22, 80, 443 et **rien d'autre**), les services et les minuteries.

### 2. Déployer le jeu — à chaque mise à jour

Clic droit sur **`deployer.ps1`** → *Exécuter avec PowerShell*.

Il envoie le code du moteur, l'orchestrateur, **les images custom** et **les
livrets PDF** (ni les unes ni les autres ne sont dans le dépôt), installe les
dépendances Python, redémarre le service, rapatrie la sauvegarde des comptes et
vérifie que le site répond.

L'étape **Documents PDF** tourne à chaque fois, `-Code` compris : ce ne sont pas
des images, et le panneau « Documents » du site serait vide sans elles. Elle
compare les tailles, n'envoie que ce qui manque — et **efface du serveur ce qui
a disparu en local**. C'est voulu, et c'est la différence avec les images : un
scan en trop ne gêne personne, un livret de règles périmé induit en erreur.

Le premier passage envoie 1,9 Go d'images, par lots de 100 Mo : c'est long, mais
une coupure ne fait perdre qu'un lot. Les fois suivantes, seules les images
nouvelles ou modifiées partent.

Variantes :

```
.\deployer.ps1 -Code      # code seul, sans les images
.\deployer.ps1 -Images    # images seules, sans redémarrage
```

---

## Les gestes du quotidien

Toutes les commandes se lancent depuis ce dossier, dans PowerShell.

```powershell
$cle = ".\cle_narwhal"; $srv = "root@178.105.177.39"

# État du site
ssh -i $cle $srv "systemctl status narwhal"

# Redémarrer (les parties en cours sont perdues, prévenez les joueurs)
ssh -i $cle $srv "systemctl restart narwhal"

# Journaux : les 100 dernières lignes, puis en direct
ssh -i $cle $srv "journalctl -u narwhal -n 100"
ssh -i $cle $srv "journalctl -u narwhal -f"

# Journaux de Caddy (certificats, routage, erreurs 502)
ssh -i $cle $srv "journalctl -u caddy -n 50"

# Place disque et poids des dossiers de parties
ssh -i $cle $srv "df -h / ; du -sh /opt/narwhal/*"

# Purge manuelle (replays et logs de plus de 30 jours)
ssh -i $cle $srv "sudo -u narwhal RACINE=/opt/narwhal JOURS=30 narwhal-purge"

# Si le disque se remplit : redimensionner les images sur le serveur
ssh -i $cle $srv "bash /opt/narwhal/redimensionner-images.sh 800"
```

Sauvegarde des comptes : automatique chaque nuit à 4 h 30, 30 archives gardées
dans `/var/backups/narwhal/`, plus une copie rapatriée dans
`Marvel LCG\sauvegardes-serveur\` à chaque déploiement.

---

## Les rapports de bug

Depuis n'importe quel écran du jeu, un bouton **« Signaler un bug »** ouvre un
formulaire : un nom (obligatoire), une description, une capture d'écran collée
en Ctrl+V ou choisie en fichier. Depuis le **plateau**, le journal de toute la
partie part avec, sans que la personne ait rien à faire.

Tout arrive sur **`https://narwhalchampions.com/admin`**, section *Rapports de
bug* : les 60 derniers, le plus récent en haut, dépliables. Trois états —
*Nouveau*, *En cours*, *Traité* — et une pastille rouge en titre tant qu'il
reste des nouveaux.

Ce qu'il faut savoir :

| | |
|---|---|
| Qui peut envoyer | **tout le monde**, y compris un invité arrivé par un lien de siège : ce sont eux qui tombent sur les bugs sans autre moyen de le dire |
| Plafond | 12 rapports par heure et par table, puis le formulaire répond « trop de rapports » |
| Texte et journal | dans `narwhal.db`, tronqués plutôt que refusés |
| Captures | fichiers dans `/opt/narwhal/site/rapports/`, un nom au hasard, servis uniquement à l'administrateur |
| Sauvegarde | les deux sont pris par la sauvegarde de nuit |
| Suppression | le bouton *Supprimer* d'un rapport efface aussi sa capture |

En **partie locale** (`JOUER-SOLO.bat`), il n'y a aucun site derrière le moteur :
le formulaire le dit et propose le presse-papier ou un fichier. Sur le plateau,
le bouton ne s'affiche pas du tout — « Log » télécharge déjà tout le déroulé.

⚠ `sauvegarde.sh` et `purge.sh` sont installés par `installer-serveur.ps1`, pas
par `deployer.ps1`. Les modifier ici ne suffit pas : il faut les réinstaller.

```powershell
scp -i $cle .\sauvegarde.sh "${srv}:/tmp/s.sh"
ssh -i $cle $srv "sed -i 's|@RACINE@|/opt/narwhal|g' /tmp/s.sh && install -m 755 /tmp/s.sh /usr/local/bin/narwhal-sauvegarde && rm /tmp/s.sh"
```

---

## Les livrets de règles

Les 27 PDF (livrets et carnets de campagne) vivent dans
`Fusion\marvel-lcg-src\assets\docs\`, hors du dépôt comme les scans. Pour en
ajouter un, déposez-le dans ce dossier et relancez `deployer.ps1` : le panneau
« Documents » le fera apparaître tout seul.

Le nom compte. Le panneau rattache un fichier à sa boîte par le **nom
d'extension qu'il contient** (`mc32_mutant_genesis_...` → Mutant Genesis), et
retombe sur le numéro `mcNN` quand le nom ne dit rien (`mc55_rulebook-web.pdf`).
Un fichier dont le nom contient `campaign-log`, `campaign_log` ou `campaignlog`
est classé comme carnet de campagne. Un PDF que rien ne rattache s'affiche
quand même, sous son nom de fichier nettoyé.

---

## Restaurer les comptes

```powershell
ssh -i $cle $srv "systemctl stop narwhal"
ssh -i $cle $srv "ls -lh /var/backups/narwhal/"        # choisir la date
ssh -i $cle $srv "cd / && tar -xzf /var/backups/narwhal/comptes-2026-09-05.tar.gz"
ssh -i $cle $srv "systemctl start narwhal"
```

Depuis une archive rapatriée sur le PC :

```powershell
scp -i $cle ..\sauvegardes-serveur\comptes-2026-09-05.tar.gz "${srv}:/tmp/"
ssh -i $cle $srv "systemctl stop narwhal && cd / && tar -xzf /tmp/comptes-2026-09-05.tar.gz && systemctl start narwhal"
```

Perte totale du serveur : recréez un VPS chez Hetzner avec la même clé SSH,
changez l'IP en tête des deux `.ps1` et dans les deux entrées DNS Cloudflare,
relancez `installer-serveur.ps1` puis `deployer.ps1`, et restaurez l'archive.
Compter une heure, dont l'essentiel en transfert d'images.

---

## Quand ça coince

| Symptôme | Cause la plus fréquente | Geste |
|---|---|---|
| Le site ne répond pas | l'orchestrateur est tombé | `journalctl -u narwhal -n 50` |
| Une table `pN` renvoie 502 | aucun moteur sur ce port : la partie est finie ou n'a jamais démarré | normal, revenez à l'accueil |
| Certificat invalide sur `p3...` | le certificat wildcard n'a pas été obtenu | `journalctl -u caddy \| grep -i cloudflare` — jeton expiré ou mauvaise permission |
| Le WebSocket se coupe | nuage orange sur Cloudflare | repassez les deux entrées DNS en **DNS only** |
| Disque plein | replays accumulés | `narwhal-purge`, puis `redimensionner-images.sh` |
| `Permission denied (publickey)` | droits de la clé privée | relancez le script, il corrige les droits |

Après un `apt upgrade`, si Caddy était remplacé, le module Cloudflare
disparaîtrait et les certificats wildcard ne se renouvelleraient plus. Le paquet
est volontairement figé (`apt-mark hold caddy`) pour cette raison.

---

## Ce qui ne doit jamais sortir de ce dossier

`cle_narwhal` (la clé privée du serveur) et `installer-serveur.ps1` (il contient
le jeton Cloudflare). Les deux sont déjà dans le `.gitignore` du projet.
