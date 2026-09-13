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

### 2. Prévenir les joueurs — dix minutes avant

**`deployer.ps1` fait `systemctl restart narwhal`, et l'orchestrateur emporte
tous ses moteurs avec lui : toute partie en cours est perdue.** Quelqu'un qui
joue n'a aucun moyen de le deviner, et son seul recours est le bouton 💾 Save
du plateau.

Sur `https://narwhalchampions.com/admin`, tout en haut, **Annonce aux
joueurs** : un délai en minutes, un message facultatif, et « Prévenir ». Si le
déploiement glisse, « Annuler l'annonce » l'efface.

Ce que voient les joueurs, dans la minute qui suit :

- **en partie**, une bande rouge barre le dixième supérieur de l'écran avec le
  décompte, **deux secondes toutes les trente**, puis s'efface complètement.
  Elle laisse passer les clics : on continue de jouer pendant qu'elle est là ;
- **sur l'écran de préparation**, le même message reste affiché en haut, sans
  clignoter : personne n'est en train de jouer, rien ne presse.

Le message par défaut dit déjà ce qu'il faut faire ; laissez le champ vide. Le
champ ne sert qu'aux annonces d'une autre nature (coupure chez l'hébergeur).

### 3. Déployer le jeu — à chaque mise à jour

Clic droit sur **`deployer.ps1`** → *Exécuter avec PowerShell*.

Il envoie le code du moteur, l'orchestrateur, **les images custom** et **les
livrets PDF** (ni les unes ni les autres ne sont dans le dépôt), installe les
dépendances Python, redémarre le service, rapatrie la sauvegarde des comptes et
vérifie que le site répond.

L'étape **Documents PDF** tourne à chaque fois, `-Code` compris : ce ne sont pas
des images, et le panneau « Documents » du site serait vide sans elles. Elle
compare les tailles, n'envoie que ce qui manque — et **efface du serveur ce qui
a disparu en local**. C'est voulu : un livret de règles périmé induit en
erreur.

Juste avant, l'étape **Uniformisation des scans** appelle
`outils/uniformiser-scans.py --appliquer` (via `wsl python3` : l'outil a des
chemins WSL codés en dur) pour ramener tout scan encore en 1500x2150 à
615 px, comme les cartes officielles. Elle ne fait rien s'il n'y a rien à
réduire, et **arrête tout le déploiement** si la sauvegarde des originaux
d'un fichier à traiter est incomplète — dans ce cas, lancez d'abord
`wsl python3 outils/uniformiser-scans.py --sauvegarde`.

L'étape **Images custom** efface aussi, depuis le passage du 06/09/2026, ce
qui a disparu en local : une image disparue ou renommée (par exemple après
une renumérotation de prefixe fan-made) est effacée du serveur, sa liste
affichée avant suppression.

Le déploiement du code rase aussi, côté serveur et juste avant d'extraire
l'archive fraîche : `Fusion/marvel-lcg-src/src`, `Fusion/marvel-lcg-src/public`
(y compris `public/app`) et les fichiers de code à la racine de `site/`
(jamais `comptes.json`, `narwhal.db` ni `site/rapports/`, qui ne voyagent
jamais dans l'archive). Sans ce rasage, un fichier renommé ou supprimé en
local serait resté sur le serveur indéfiniment.

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

Sauvegarde : automatique chaque nuit à 4 h 30, 30 archives gardées dans
`/var/backups/narwhal/`, plus une copie rapatriée dans
`Marvel LCG\sauvegardes-serveur\` à chaque déploiement. Depuis le 06/09/2026,
elle couvre aussi les decks, campagnes, hauts faits et replays des joueurs
(pas seulement `site/`), et prend `narwhal.db` par un instantané SQLite
cohérent plutôt qu'une copie brute (le moteur y écrit sans arrêt, en mode
WAL). Vérifier qu'une sauvegarde restaure vraiment quelque chose :

```
ssh -i $cle $srv "sudo -u narwhal RACINE=/opt/narwhal narwhal-sauvegarde --verifier"
```

---

## Le mode Legacy

Sixième tuile de l'accueil. On commence avec la boîte de base et ses cinq
héros, et on ouvre la suite boîte par boîte en gagnant : tous les vilains de la
vague battus, tous ses héros vainqueurs. Ce qui est fermé reste visible, grisé,
avec le nom de sa boîte ; la condition complète est en infobulle et dans le
bandeau jaune en tête de l'étape.

Les héros fan-made s'achètent : une première victoire avec un héros officiel
donne un jeton, deux en expert. Un clic sur un fan-made grisé le débloque.

**Le deck-building suit.** Dans l'éditeur de deck ouvert depuis Legacy, les
cartes des boîtes pas encore ouvertes sont grisées et ne s'ajoutent pas. À
l'étape des decks, un deck tout fait qui en contient une est caché : les
paquets d'aspect du tableur piochent dans toutes les vagues, aucun ne passe au
Set de base, il reste le deck de base et ce qu'on construit soi-même.

La progression de chacun vit dans `legacy-serveur-N.json`, à côté de son
historique. Le fichier ne contient que ce qui ne se déduit pas de l'historique
(date de départ, jetons dépensés) : le reste se recalcule à chaque ouverture.
Le supprimer ne fait perdre que ces deux choses.

## Les parties terminées, et comment les revoir

Depuis le 13/09/2026, **chaque partie terminée laisse un enregistrement
complet**, écrit tout seul par le moteur. On la revoit pas à pas avec le bouton
**« Revoir »** de l'écran de préparation, exactement comme si on y était.

Ils vivent dans `replays/serveur-N/`, un dossier par compte. On en garde les
**cinquante plus récents** par personne (`SAUVEGARDES_GARDEES`) : un
enregistrement pèse environ 44 Ko, donc 2 Mo par compte et 44 Mo pour les vingt
places.

⚠ **Les trois emplacements du plateau (Save 1, 2, 3) ne sont jamais emportés par
ce ménage.** Ce sont des sauvegardes voulues, posées à la main.

⚠ Ils partent en revanche avec la place quand un compte expiré se la fait
reprendre : `_nettoyer_emplacement` vide le dossier.

## Les tables qui ne servent plus

Une table allumée tient un port, un processus et sa mémoire, sur vingt places.
Deux minuteurs la ferment :

- **Huit heures d'âge**, quoi qu'il arrive (`DUREE_MAX_HEURES`) ;
- **Trois quarts d'heure sans jouer** (`INACTIVITE_MINUTES`, 45 par défaut).
  **Ta table à toi n'est jamais fermée pour inactivité** : elle sert à regarder
  ce qui se passe, souvent sans y jouer.

⚠ **Le signal est le journal du moteur, pas le « vu » du site.** Celui-ci ne
bouge qu'à l'ouverture du jeu : pendant qu'on joue, le navigateur parle au
moteur et le site n'entend plus rien. S'y fier aurait fermé la table de
quelqu'un en pleine partie. Une table dont on n'arrive pas à lire le journal
n'est jamais fermée au hasard.

**La partie est sauvegardée avant que la table se ferme**, quel que soit le
motif. Le joueur la retrouve sous « Reprendre ». À huit heures on pouvait s'en
passer, à trois quarts d'heure non.

Mettre `INACTIVITE_MINUTES=0` dans le service éteint cette règle sans toucher au
reste.

## Les comptes qui dorment

Il n'y a que vingt places, et une place n'est pas qu'une ligne dans une base :
c'est un **espace de jeu**, avec ses decks, ses campagnes en cours et ses hauts
faits.

**Quatre semaines sans venir, et le compte passe en « expire ».** Sa session se
ferme, sa table s'éteint, il ne compte plus dans le quota. Mais **il n'est pas
supprimé** : sa ligne reste dans `/admin`, et son espace de jeu l'attend tant
que personne n'a pris sa place.

Sa place n'est reprise qu'au moment où quelqu'un en a besoin, et elle est
effacée à ce moment-là seulement. Si la personne revient avant, elle retrouve
tout.

**Pour la remettre en service** : bouton « Valider » sur sa ligne dans
`/admin`. Si sa place a déjà été donnée, elle en reçoit une neuve et repart de
zéro.

La colonne **Dernière visite** est ce qui décide : elle suit l'ouverture du jeu,
pas la saisie du mot de passe. Une session dure trois mois, donc quelqu'un qui
joue tous les soirs sans jamais retaper son mot de passe reste bien « vu
aujourd'hui ».

Le site ne sait pas envoyer de courriel : personne ne peut être prévenu de son
expiration. La règle est donc écrite sur l'écran de connexion, où tout le monde
passe.

Pour changer le délai : variable d'environnement `EXPIRATION_JOURS` du service
(28 par défaut).

## Écrire à un joueur

Dans `/admin`, section **Joueurs** : qui est là, et la conversation avec chacun.
Un bloc par compte, l'échange complet, et une case pour répondre. Ceux qui ont
un message en attente s'ouvrent tout seuls, avec une pastille.

Le message part tout de suite. **La personne voit une pastille verte en bas à
droite de son écran**, dans l'assistant comme en pleine partie, qui ouvre la
conversation dans un nouvel onglet. Elle disparaît dès qu'elle est lue.

⚠ **Ce n'est pas le retour du tchat**, retiré du jeu le 12/09/2026. Rien ne
s'affiche tant que personne n'écrit : la pastille n'existe que lorsqu'un
message attend vraiment.

Répondre depuis `/admin` marque aussi la conversation comme lue de ton côté :
sans cela ta propre pastille restait allumée sur un échange que tu venais de
traiter.

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

## Le suivi des parties sur ton téléphone

`https://narwhalchampions.com/suivi`, réservé au compte administrateur
(même règle que `/admin`). La page liste les tables allumées (qui, quel héros,
quel méchant, le round, les PV, depuis quand) puis les quarante dernières
parties terminées (héros, aspect du deck, méchant, rounds, victoire ou
défaite). Elle se rafraîchit toutes les 30 secondes.

Pour en faire une icône d'appli : ouvrir la page dans Chrome sur le téléphone,
menu ⋮ puis « Ajouter à l'écran d'accueil ». Elle s'ouvre ensuite plein écran,
sans barre d'adresse.

| Où ça vit | Quoi |
|---|---|
| `site/orchestrateur.py`, routes `/suivi`, `/api/suivi`, `/suivi.webmanifest` | la page et son flux JSON |
| `games_history-serveur-<N>.json` à la racine du jeu | une partie terminée par ligne, écrite par le moteur de la table N |
| `/get_partie_en_cours?jeton=…` sur chaque moteur | la fiche d'une partie en cours, interrogée en local par le site |

Les parties **abandonnées** y figurent aussi, en orange, avec le round atteint,
les PV du héros et du méchant au moment où on a quitté, et la cause : table
éteinte par le joueur, fermée après 8 h, moteur arrêté, redémarrage du site.
La photo est prise juste avant de tuer le moteur ; une table qu'on ferme sans
avoir lancé de partie ne laisse rien.

L'aspect du deck n'est enregistré que depuis le 08/09/2026 : les parties
plus anciennes s'affichent sans lui.

⚠ La colonne « Fermée le » de la page d'administration annonçait « en cours »
pour toujours sur les tables tuées par un redémarrage du site : la fermeture
n'était notée que par le faucheur et par le bouton « Éteindre ». Corrigé le
08/09/2026, et les lignes restées ouvertes sont fermées au démarrage suivant,
avec l'heure de ce démarrage faute de mieux.

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

## Les originaux des scans fan-made

Les scans livrés par les auteurs (1500 x 2150, 2,3 Go pour 2492 fichiers) ne
sont pas dans le dépôt et ne sont plus servis tels quels : `outils/uniformiser-scans.py`
les réduit à 615 px de petit côté avant envoi. Ils existent à deux endroits :

- sur le poste, `sauvegardes-serveur/scans-originaux/` (ignoré par git) ;
- sur le serveur, `/var/backups/narwhal/scans-originaux/`, copie faite le
  07/09/2026 par `rsync`, à refaire après tout nouvel import d'images
  (`rsync -a --partial -e "ssh -i deploiement/cle_narwhal" sauvegardes-serveur/scans-originaux/ root@<ip>:/var/backups/narwhal/scans-originaux/`).

Sans eux, une nouvelle réduction (autre cible que 615) serait impossible sans
perte : l'outil refuse d'ailleurs de tourner si la sauvegarde est incomplète.
