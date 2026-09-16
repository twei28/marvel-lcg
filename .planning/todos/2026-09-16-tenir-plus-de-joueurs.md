# Tenir plus de joueurs : ce qui a été mesuré, et ce qui a été écarté

Question de l'utilisateur, 16/09/2026 : « si j'enlève la limite de 20 places,
je pourrai avoir combien de joueurs en même temps ? », puis « comment passer à
100 sans payer plus ? ».

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

### Ce que cela donne en sièges

Le plafond n'est pas la mémoire, c'est le LOGICIEL : `NB_EMPLACEMENTS` vaut 20,
et le Caddyfile porte 20 routes `p1..p20` écrites à la main.

| | Tables | Joueurs (4 par table) | Mémoire attendue |
|---|---|---|---|
| **Aujourd'hui, sans rien changer** | 20 | **80** | ~2,2 à 2,8 Go, tient sur la machine |
| En levant le plafond logiciel | 40 | 160 | ~4,8 Go, **demande 8 Go** |

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
