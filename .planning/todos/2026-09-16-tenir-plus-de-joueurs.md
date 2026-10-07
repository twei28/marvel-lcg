# Tenir plus de joueurs : ce qui a été mesuré, et ce qui a été écarté

Question de l'utilisateur, 16/09/2026 : « si j'enlève la limite de 20 places,
je pourrai avoir combien de joueurs en même temps ? », puis « comment passer à
100 sans payer plus ? ».


## ⚠ CORRECTION DU 06/10/2026 (soir) : le banc de charge interrogeait la MAUVAISE route

Le banc (`outils/charge-serveur.py`) lisait « le monde » par `/get_partie_en_cours`. **C'est une petite
route de suivi du site** (`server_get.py`, `get_partie_en_cours` : une fiche de quelques champs), pas
le monde. Le plateau lit la partie par **`/get_world`** (`ui-app/src/board/sources.ts`,
`chargerPartieEnCours`) : le descripteur COMPLET du monde, masqué par siège puis compressé en gzip,
à CHAQUE trame et pour chaque client.

Conséquences, à relire avant de s'appuyer sur les sections ci-dessous :
1. **Le test de charge de 18 minutes SOUS-ESTIME la charge réelle** : la sérialisation et la
   compression du monde (`Json.DumpGZip`, `MasquerCeQuOnNaPasLeDroitDeVoir`) n'y étaient pas. Le
   plafond réel est probablement PLUS BAS que ~25 à 40 tables jouées. Non remesuré.
2. **Le constat du profil « la part web pèse ~2 % » est invalide** pour de vrais joueurs : le profil
   a été pris sans aucune requête `/get_world`. Ce qui reste vrai : `Present` →
   `deck_to_descriptors` (~75 % du fil du jeu) tourne à chaque événement, requête ou non. S'y ajoute,
   en vrai, la sérialisation du monde par client, non mesurée.
3. **L'hypothèse de départ (« la relecture du monde coûte ») n'était donc pas réfutée**, seulement
   non testée. Elle redevient plausible.

Le script est corrigé (`/get_world?hot_seat&p=0`). **À refaire : le banc de charge avec la bonne
route, puis un nouveau profil.**

## Les mesures, toutes prises le jour même

| Quoi | Valeur |
|---|---|
| Machine | CX23 : 2 vCPU, 3,8 Go, **aucun swap**, 28 Go libres sur le disque |
| Une table au repos | ~~221 Mo~~ → **70 Mo** (corrigé le 16/09, voir le banc d'essai ci-dessous) |
| Une partie montée et jouable | **81 Mo** |
| Tables simultanées tenables | ~~~14~~ → **~40** sur la machine actuelle |
| `PLACES_MAX` | 20, mais c'est un nombre de COMPTES, pas de parties simultanées |

⚠ **LA MESURE DE 221 Mo ÉTAIT FAUSSE, et elle a servi à décider.** Elle
additionnait des RSS sans tenir compte des pages PARTAGÉES : dix processus
Python qui chargent le même moteur ne paient le code qu'une fois. Refaite au
banc d'essai le 16/09/2026, table par table, la vraie valeur est **70 Mo au
repos et 81 Mo une fois la partie montée**. Le plafond de tables n'était donc
pas ~14 mais **~40** sur cette machine.

## Le banc d'essai du 16/09/2026

Demande de l'utilisateur : « simule 100 parties en même temps et calcule la
latence ». Cent parties demandent plus de mémoire que la machine n'en a : on a
donc monté la charge pour de vrai jusqu'à la limite sûre, et extrapolé sur des
mesures. Dix tables ouvertes sur les **places 11 à 20** (libres, aucun compte,
aucun dossier de données), chaque processus d'essai portant
`oom_score_adj = 1000` pour que le tueur de mémoire le vise lui, et jamais le
site.

**Le coût d'une partie, étape par étape** (dans un seul processus) :

| Étape | RSS |
|---|---|
| Processus Python nu | 10 Mo |
| Modules du moteur importés | 50 Mo |
| Moteur initialisé (5590 cartes) | 68 Mo |
| Scène créée | 68 Mo |
| **Partie montée et jouable** | **81 Mo** |

**La montée en charge, dix tables** : 697 Mo de RSS cumulé, mais seulement
**499 Mo réellement pris** à la machine (3209 → 2710 Mo libres). L'écart, c'est
le partage de pages — et c'est précisément ce que la mesure de 221 Mo avait
manqué.

**La latence sous charge**, clients tapant en continu sur les dix tables :

| Clients | Requêtes/s | Tables (médiane) | p95 | Site (médiane) | Charge | Erreurs |
|---|---|---|---|---|---|---|
| 10 | 182 | 3,8 ms | 8,7 ms | 3,4 ms | 0,55 | 0 |
| 20 | 362 | 3,4 ms | 11,3 ms | 3,1 ms | 1,09 | 0 |
| 40 | 646 | 4,8 ms | 30,0 ms | 3,8 ms | 2,00 | 0 |
| 80 | 748 | **32,9 ms** | 126,8 ms | 9,5 ms | 4,95 | 0 |

⚠ **Le point de bascule est à 40 clients**, là où la charge atteint 2,00, soit
exactement le nombre de vCPU. Au-delà, la latence médiane est multipliée par
sept et le débit ne monte presque plus (+16 % pour deux fois plus de clients).
**Zéro erreur partout** : la machine ralentit, elle ne casse pas.

**Ce que cela donne pour 100 parties** : ~6 à 8 Go de mémoire (le partage
faiblit quand les parties divergent), donc **un CX32 à 8 Go est juste, un CX42
à 16 Go est confortable**. Côté CPU il n'y a aucun problème : depuis le
sondage adaptatif, 100 parties à deux joueurs produisent une quinzaine de
requêtes par seconde, contre ~650 tenues par la machine.

### Le cache d'images, mesuré à son tour

⚠ **`Cache.cache` (`src/engine/file/cache.py`) est un dictionnaire SANS BORNE** :
chaque image chargée y reste pour la vie du processus de la table. C'est ce que
le premier banc ne voyait pas, ses tables n'ayant jamais servi une carte.

| Cartes vues par la table | RSS du moteur |
|---|---|
| 0 (cache vide) | 68 Mo |
| 100 | 70 Mo |
| 300 | 78 Mo |
| 600 | 86 Mo |
| 1200 | **102 Mo** |

Soit **~29 Ko par carte vue**, linéaire, et jamais rendu. Conséquences :

- une table fraîche avec une partie montée : **81 Mo** ;
- une table où quatre joueurs enchaînent une soirée (héros et scénarios
  variés, 1000 à 2000 cartes distinctes) : **110 à 140 Mo** ;
- le pire cas théorique, toutes les cartes du jeu vues sur la même table :
  5927 × 29 Ko ≈ 170 Mo de cache, soit ~240 Mo. **C'est très probablement ce
  que mesurait le chiffre de 221 Mo** : non pas une table au repos, mais une
  table qui avait beaucoup servi.

⚠ **Première tentative de cette mesure, ratée et instructive** : les images
étaient demandées par HTTP sans cookie de session, et le moteur répondait sa
page de mot de passe (1,8 Ko). Neuf cents requêtes plus tard le RSS n'avait pas
bougé d'un octet, ce qui se lisait comme « le cache ne coûte rien ». Il ne
coûtait rien parce que rien n'avait été servi. La mesure a été refaite sur
`Cache.LoadImage` directement.

## Le test de RUPTURE du 16/09/2026

Demande de l'utilisateur : « fais un vrai pain test ». Donc sans garde-fou :
ouvrir des tables jusqu'à ce que ça casse, chacune avec **800 cartes servies
dans son cache** pour peser ce que pèse une vraie table de soirée.

⚠ **Deux protections, et elles ne sont pas cosmétiques** : l'orchestrateur a
reçu `oom_score_adj = -1000` (le tueur de mémoire ne doit jamais choisir le
témoin) et chaque table d'essai `+1000` (c'est elle qu'on sacrifie). Remis à
zéro à la fin.

**Résultat : 70 tables ouvertes, AUCUNE RUPTURE.** Le test a atteint son propre
plafond avant que la machine ne cède.

| Tables | Libre | Swap | Latence du site | Démarrage | RSS cumulé |
|---|---|---|---|---|---|
| 5 | 2874 Mo | 25 Mo | 1,8 ms | 2 s | 488 Mo |
| 20 | 1654 Mo | 25 Mo | 2,1 ms | 2 s | 1946 Mo |
| 35 | 433 Mo | 25 Mo | 1,4 ms | 2 s | 3419 Mo |
| 45 | 103 Mo | 424 Mo | 2,3 ms | 2 s | 3664 Mo |
| 60 | 109 Mo | 1677 Mo | 2,5 ms | 2 s | 3903 Mo |
| **70** | **94 Mo** | **2462 Mo** | **1,6 ms** | **3 s** | **4104 Mo** |

Ce que ces chiffres disent :

- **la latence du site n'a pas bougé d'un bout à l'autre** : 1,2 à 3,2 ms, y
  compris à 70 tables et 2,4 Go de swap. Le démarrage d'une table non plus
  (2-3 s à la soixante-dixième comme à la première) ;
- **zéro erreur, zéro OOM** ;
- le RSS cumulé (4104 Mo) **dépasse la RAM physique** (3815 Mo) : c'est le
  partage de pages, encore lui, plus le swap ;
- le système s'auto-régule : à partir de la 40ᵉ table, la mémoire libre se
  stabilise vers 100 Mo et le swap prend le relais, ~88 Mo par table
  supplémentaire. Il restait 1,6 Go de swap, soit **une rupture attendue vers
  85-90 tables**.

⚠ **ET VOICI LA LIMITE DE CE TEST, QUI COMPTE AUTANT QUE SON RÉSULTAT.** Ces 70
tables sont **ouvertes, pas jouées** : aucun client ne s'y connecte, les pages
swappées restent froides, et c'est précisément pourquoi le swap ne coûte rien.
**70 tables où l'on JOUE vraiment, c'est une tout autre mesure** : les pages
redeviendraient chaudes, et le swap passerait de filet à goulot. Le banc de
charge (plus haut) situe déjà la bascule CPU à 40 clients tapant en continu.

Ne pas conclure « la machine tient 280 joueurs ». Conclure : **la mémoire
n'est pas le mur qu'on croyait**, et le mur réel est le CPU sous jeu réel.

### Ce que cela donne en sièges

Le plafond n'est pas la mémoire, c'est le LOGICIEL : `NB_EMPLACEMENTS` vaut 20,
et le Caddyfile porte 20 routes `p1..p20` écrites à la main.

| | Tables | Joueurs (4 par table) | Mémoire attendue |
|---|---|---|---|
| **Aujourd'hui, sans rien changer** | 20 | **80** | large : 70 tables ont tenu au test de rupture |
| En levant le plafond logiciel | 40 à 70 | 160 à 280 | tient en mémoire, **non vérifié sous jeu réel** |

⚠ **Ce que le banc n'a toujours PAS mesuré** : le trafic WebSocket des actions
de jeu (seules les requêtes HTTP l'ont été) et la pointe de CPU que feraient
cent démarrages simultanés.

## Le vrai goulot n'était pas la mémoire

Relevé sur les journaux de Caddy, 3,2 heures : **`/get_choix_sieges` pesait
5917 requêtes, soit 61 % de tout le trafic vers les tables**, à raison d'une
toutes les deux secondes et par client. Y compris en solo, y compris onglet
caché, y compris quand rien ne bouge. À cent joueurs, cinquante requêtes par
seconde, chacune réveillant un processus Python.

Et ces appels **empêchaient les tables de s'éteindre** : le faucheur juge
l'inactivité sur la date du journal du moteur, que chaque requête fait vivre.

Corrigé le jour même (sondage adaptatif : rien si l'onglet est caché, 2 s en
attente dans un salon, 15 s sinon).

## Ce qui a été écarté, et pourquoi

**Rendre le moteur multi-parties** : ÉCARTÉ par l'utilisateur le 16/09/2026.

Le chiffrage, pour mémoire :

- **204 000 lignes de cartes n'auraient PAS à bouger** : les 5590 cartes
  n'utilisent aucune globale, elles reçoivent `effect` en paramètre. Vérifié :
  zéro fichier de `src/cards` ne cite `Engine.game` ni `Engine.statistics`.
- Le cœur à reprendre : 66 000 lignes (`src/engine` + `src/game`), 64 accès
  globaux, **126 variables de configuration** dont une dizaine sont propres à
  chaque place, plus toute la couche web (un serveur = une partie aujourd'hui).
- Durée estimée : **deux à trois mois** à temps plein.
- ⚠ **Le risque n'est pas le temps, c'est la fuite entre parties.** L'isolation
  par processus donne aujourd'hui gratuitement une garantie forte : une partie
  ne peut pas en voir une autre, le système d'exploitation l'en empêche. Un
  correctif du 15/09 (« la main d'un joueur ne sort plus du moteur ») montre
  que ce genre de défaut existe même AVEC cette isolation.
- En face : ~480 €/an pour une machine à 32 Go, qui tiendrait ~145 tables.

## Ce qui reste possible, gratuitement

1. ✅ **Fait** : le sondage du salon, divisé par ~15.
2. ✅ **Fait** : `.site` exclu du déploiement, pour que le faucheur cesse d'être
   aveugle après chaque mise à jour.
3. ✅ **Fait** : **4 Go de swap**, en place et vérifiés sur le serveur le
   16/09/2026 (`free -m` : 4095 Mo, 0 utilisé). C'est surtout un filet contre le
   tueur de mémoire, qui auparavant aurait frappé au hasard.
4. **zram** : ⚠ **posé mais inactif** — le noyau du serveur n'embarque pas le
   module (`lsblk` ne montre aucun zram). Il faut `apt install
   linux-modules-extra-$(uname -r)`, décision en attente de l'utilisateur. Le
   script calcule en conséquence : `swappiness` est à **60** (valeur sans
   zram), et non à 100.
5. ✅ **Fait** : `INACTIVITE_MINUTES` passé de 45 à **30** le 16/09/2026.
6. **Fermer une table dont plus aucun client ne tient la WebSocket**, sans
   attendre le seuil d'inactivité.
7. **Redimensionner à la demande** : Hetzner facture à l'heure et sait agrandir
   une machine existante, le temps d'une soirée chargée.

## Statut

**Cadré et mesuré le 16/09/2026.** La refonte multi-parties est ÉCARTÉE.

Faits : **1, 2, 3 et 5**. En attente d'une décision : **4** (une commande
`apt` à lancer). Restent disponibles, non engagés : **6** (fermer une table
que plus aucun client ne tient) et **7** (redimensionner à l'heure).

⚠ Correction du 16/09/2026 : cette fiche annonçait « les points 3 à 7 restent
disponibles, aucun n'est engagé » alors que le swap et le seuil d'inactivité
étaient déjà livrés. Relevé en relisant le serveur, pas la fiche.

## Test de charge JOUÉ du 06/10/2026 : 100 tables, ça NE TIENT PAS

Demande de l'utilisateur : « voir si ça tient, sinon trouver une solution ». Tables jouées en vrai
par des bots via WebSocket (`outils/charge-serveur.py`, lancé en `narwhal`, places 161+, ports 2511+,
sur le vrai serveur pendant que des joueurs pouvaient jouer). Montée de 10 en 10 toutes les 60 s,
18 minutes en tout. Mesures brutes : `.planning/todos/2026-10-06-charge-serveur-resultats.jsonl`.

| Tables vivantes | Charge (2 vCPU) | Latence p95 d'un coup | Latence p95 du monde | Mémoire libre / swap |
|---|---|---|---|---|
| 10 | 0,7 | 11 ms | 3 ms | 2150 Mo / 54 Mo |
| 22 | 7,9 | 22 ms | 19 ms | 1170 Mo / 76 Mo |
| 26 | 11,7 | 57 ms | 59 ms | 825 Mo / 146 Mo |
| 33 | 13,2 | 194 ms | 157 ms | 147 Mo / 302 Mo |
| 43 | 15,7 | 359 ms | 331 ms | 83 Mo / 1609 Mo |

- **Le mur est le CPU, pas la mémoire.** Charge de 8 à 17 sur 2 vCPU. Une table jouée coûte
  ~60 à 75 Mo (PSS), donc la mémoire tenait jusqu'à ~40 tables.
- **Dégradation visible dès ~22 tables jouées, mauvaise à ~33, saturée à ~43.** Au-delà de ~44, les
  nouvelles tables n'ont jamais répondu dans les 240 s (le démarrage d'un moteur coûte du CPU) et
  le nombre de tables vivantes est retombé à 25.
- **Le site (orchestrateur) est resté à 2 à 18 ms** : le goulot est le moteur.
- **Le client qui pèse le plus** : `/get_partie_en_cours` (le monde complet) est relu à CHAQUE trame,
  ~2,5 requêtes par seconde et par table, contre ~0,15 pour les coups. C'est le premier suspect.

⚠ **Limites du test, qui le rendent plus sévère que la réalité** : les bots tournent sur la même
machine et lui prennent du CPU (part non mesurée) ; leurs parties durent ~25 s (le bot perd vite),
donc elles enchaînent des créations de partie, bien plus coûteuses qu'une partie humaine de 30 min ;
ils jouent des coups au hasard. Le vrai plafond est donc plus haut que ~25 à 30 tables jouées, mais
**pas de 100**. Non mesuré : les pertes de tables sur arrêt du moteur, la part CPU du banc.

## Pistes pour tenir plus (à valider, rien n'est engagé)

1. **Alléger la trame** : ne pas resserialiser tout le monde à chaque trame (diff, ou cache par
   `render_id` partagé entre les clients d'une même table). À profiler d'abord (`py-spy` sur une table
   sous charge) pour confirmer que c'est bien la sérialisation du monde.
2. **Plus de cœurs** : Hetzner redimensionne à l'heure. Le CPU étant le mur, viser des vCPU
   dédiés plutôt que de la RAM.
3. **Plusieurs machines** : l'orchestrateur aiguille déjà par place ; répartir les places sur
   plusieurs serveurs. Plus de travail, mais le seul chemin au-delà d'une machine.
4. **Relancer le banc** après chaque piste, avec les bots sur une AUTRE machine pour ne plus fausser
   la mesure.

## Profil du moteur sous charge, 06/10/2026 (⚠ voir la correction en tête de fiche : pris SANS requête /get_world)

Mesure : py-spy (installé en dossier temporaire, retiré après), 40 s à 100 Hz sur UN moteur de table
jouée, 17 tables jouées en même temps (banc `outils/charge-serveur.py`, places 261+).

⚠ **Ce que l'on croyait** : le navigateur relit le monde complet à chaque trame
(`/get_partie_en_cours`, ~2,5 fois par seconde et par table), et c'est cela qui coûte. **Non.** La part
web (aiohttp, envoi des trames) est de l'ordre de 2 % des échantillons.

**Ce qui coûte vraiment** : `WorldRender.PresentInternal` (`game/world/world_render.py:107`) reconstruit
le descripteur de TOUT le monde à CHAQUE événement du moteur, qu'un client demande quelque chose ou non :
`ToDescriptor.World` → `Player` → `deck_to_descriptors` → `ToDescriptor.Card` → `Card.Render`
(`game/render/to_descriptor.py:12`, `:162` ; `game/card/card.py:891`), pour CHAQUE carte de CHAQUE pile
(paquet joueur de 40 cartes, défausses, pile rencontre, main, zones), y compris les piles qui n'ont pas
bougé ni ne sont visibles.

| Part des échantillons | Quoi |
|---|---|
| **37 %** | `Present` (reconstruction du descripteur) ; **34 %** dans `deck_to_descriptors` seul |
| 32 % | `ToDescriptor.Card` ; dont 22 % dans `Card.Render` |
| ~21 % | boucle de jeu et résolution des effets (la logique de jeu elle-même) |
| ~16 % | création de partie (gonflé par le banc : ses parties durent 25 s) |
| ~43 % | un fil `_worker` (probablement en attente, compté à tort) |

En ne gardant que le fil du jeu (48 % du total), **le rendu pèse ~75 % de son temps**. Le rendre
presque gratuit pourrait doubler à tripler la capacité ; ce n'est pas mesuré, seulement estimé.

**Pistes de correction, par ordre de risque croissant** (rien n'est engagé) :
1. Ne pas détailler carte par carte les piles cachées ou inchangées (paquet joueur, pile rencontre) :
   ne garder que le décompte, SI le plateau n'a pas besoin de leur contenu (à vérifier : recherche
   dans le paquet, « voir la défausse »).
2. Un compteur de version par pile (`Deck`), qui n'est incrémenté que sur un déplacement, pour réutiliser
   le descripteur de la pile entière quand elle n'a pas changé.
3. Un cache par carte avec invalidation (le plus risqué : l'état d'une carte dépend de beaucoup de choses).

⚠ Le descripteur est par SIÈGE (la main d'un joueur ne doit jamais sortir du moteur, correctif du
15/09) : tout cache doit le respecter. Toucher à ce chemin impose `tools/test_capacites.py` et un
passage par le plateau (étape 8 bis de PROCESSUS-CARTE).

Note du 06/10/2026 : `outils/charge-serveur.py` appelle maintenant `/get_world` (la vraie charge) ET
`/get_partie_en_cours` (petite fiche, uniquement pour détecter la fin de partie et enchaîner la
suivante). Non rejoué depuis la correction.
