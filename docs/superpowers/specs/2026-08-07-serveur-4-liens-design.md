# Serveur 4 liens : héberger le jeu classique pour des amis

Date : 2026-08-07
Statut : spec validée, à planifier

## Le besoin

Aujourd'hui il existe deux façons de lancer le jeu :

- `JOUER-SOLO.bat` : un moteur sur le port 2345, accessible seulement depuis le PC hôte.
- `JOUER-EN-MULTI.bat` : un moteur sur le port 2347, un tunnel Cloudflare, un salon, des sièges
  protégés. Tout le monde joue **la même partie**.

Il manque un troisième usage : tant que le jeu tourne chez l'hôte, des amis doivent pouvoir
**accéder au jeu** par un lien et y faire ce qu'ils veulent, chacun de son côté, en mode
classique. Pas de salon, pas de sièges, pas de partie partagée : le lien ouvre l'assistant de
création de partie, et l'ami crée sa partie, joue en solo ou en hotseat, et reprend sa
sauvegarde plus tard.

## Décisions prises

| Question | Décision |
|---|---|
| Où arrive l'ami ? | Sur `/prepare.html`, l'assistant de création de partie classique |
| Combien en parallèle ? | 4 amis, chacun sa partie, sans se gêner |
| Adresses | Tunnels temporaires `trycloudflare`, liens neufs à chaque lancement |
| Sauvegardes | Séparées par lien |
| Decks | L'ami voit les decks de l'hôte et les siens, et n'écrit que dans son dossier |
| Mot de passe | Aucun. Le lien suffit |
| Place de l'hôte | Hors des 4 places. Il continue par `JOUER-SOLO.bat` sur le port 2345 |

Les adresses fixes ont été étudiées et écartées : Tailscale Funnel plafonne à trois ports
publics (443, 8443, 10000), ngrok gratuit plafonne à 20 000 requêtes et 1 Go par mois, ce qui ne
tient pas une soirée de jeu, localtunnel ne réserve pas les sous-domaines, et un tunnel
Cloudflare nommé exige un nom de domaine payant.

## Architecture

### Un moteur par place

Le moteur est mono-partie : un processus Python égale une partie. Quatre places veut donc dire
**quatre processus**, sur les ports **2351 à 2354**, choisis hors du 2345 (solo) et du 2347
(multi) pour que les trois modes puissent cohabiter.

### Isolement par la configuration, pas par le code

Aucune modification du moteur n'est nécessaire. Tout passe par quatre fichiers de configuration
dérivés de `launch.json` au démarrage, écrits dans `Fusion/marvel-lcg-src/.serveur/launch-N.json`
(N de 1 à 4). Dériver plutôt que dupliquer évite que ces fichiers divergent de `launch.json`
quand l'hôte y modifie un chemin d'images ou un réglage.

Réglages remplacés pour l'instance N :

| Clé | Valeur | Effet |
|---|---|---|
| `server_addresses` | `["127.0.0.1:235N"]` | un port par instance |
| `replay_folders` | `["../replays/serveur-N/"]` | sauvegardes séparées |
| `games_history_file` | `"../games_history-serveur-N.json"` | historique séparé |
| `game_statistics_file` | `"../statistics-serveur-N.json"` | statistiques séparées |
| `deck_folders` | `["./deck/serveur-N/", "./deck/custom/"]` | écrit chez lui, lit aussi chez l'hôte |
| `password` | `""` | aucun mot de passe d'entrée |
| `seat_passwords` | `[]` | aucun siège réservé, le lien mène droit au jeu |

Le reste (images, sons, catalogue de cartes, decks de départ, traduction) est hérité de
`launch.json` et donc commun.

La ligne `deck_folders` repose sur un comportement vérifié du moteur : `save_deck` écrit dans
`deck_folders[0]` (`src/engine/device/web/server/server_get.py:52`) tandis que `list_deck` liste
**tous** les dossiers de la liste (`server_get.py:36`). L'ami construit donc ses decks dans son
dossier et voit ceux de l'hôte, sans pouvoir les modifier ni les supprimer. Les amis ne voient
pas les decks les uns des autres, ce qui écarte tout risque de collision de noms de fichiers.

### Le lanceur

`Fusion/marvel-lcg-src/launcher-serveur.sh`, construit sur la mécanique déjà éprouvée de
`launcher-multi.sh` :

1. Vérifie que `python3.10` et `cloudflared` sont présents et exécutables.
2. Accepte un argument optionnel : le nombre de places, de 1 à 4, par défaut 4.
   `./launcher-serveur.sh 2` ne monte que deux moteurs, utile si le PC peine.
3. Génère les configurations et crée les dossiers `replays/serveur-N/` et `deck/serveur-N/`.
4. Démarre les moteurs, journal séparé dans `/tmp/marvel-serveur-N.log`, et attend que chacun
   réponde en HTTP avant de continuer.
5. Ouvre un tunnel par moteur et récupère l'adresse `https://xxxx.trycloudflare.com`.
6. Affiche les liens numérotés, sous la forme `https://xxxx.trycloudflare.com/prepare.html`, et
   copie le message dans le presse-papier via `clip.exe`.
7. `trap` sur EXIT, INT et TERM : tue les moteurs et les tunnels, et le dit.

**Dégradation choisie** : si un moteur ou un tunnel ne monte pas, le lanceur le signale et
continue avec les autres. Trois liens valent mieux que zéro. Le lanceur ne s'arrête que si
**aucune** place n'a pu être ouverte.

`JOUER-SERVEUR.bat` à la racine appelle ce script dans WSL, sur le modèle exact de
`JOUER-EN-MULTI.bat`.

## Limites assumées

- **Sans mot de passe, quiconque a le lien entre.** Le lien est aléatoire et change à chaque
  lancement, ce qui borne la casse. Le réglage `password` reste dans la configuration si l'hôte
  change d'avis.
- **Deux personnes sur le même lien tombent sur la même partie** et se marchent dessus. La
  convention est un lien par personne. Rien ne l'impose techniquement.
- **Le PC hôte fait tourner quatre jeux plus quatre tunnels.** La consommation réelle sera
  mesurée au premier essai. L'argument « nombre de places » est la soupape.
- **Une place égale une partie à la fois.** Un ami qui veut deux parties en cours doit en
  sauvegarder une et charger l'autre.
- **Rien n'est exposé hors de la durée du script**, comme en mode multi.

## Tests

Le seul point qui peut mal tourner en silence, c'est l'isolement : une configuration
approximative donnerait quatre moteurs qui se partagent le même dossier de sauvegardes sans que
personne ne s'en aperçoive avant qu'une partie soit écrasée.

`Fusion/marvel-lcg-src/tools/test_serveur_multi.py` monte deux instances et vérifie :

1. **Cas nominal** : les deux moteurs répondent, chacun sur son port.
2. **Sauvegardes cloisonnées** : une partie sauvegardée sur l'instance 1 n'apparaît pas dans la
   liste de l'instance 2.
3. **Decks partagés en lecture** : un deck présent dans `deck/custom/` apparaît dans la liste des
   deux instances.
4. **Decks protégés en écriture** : un deck enregistré depuis l'instance 1 atterrit dans
   `deck/serveur-1/` et non dans `deck/custom/`.
5. **Cas limite** : le lanceur appelé avec un nombre de places hors bornes (0, 5, texte) le
   refuse avec un message clair au lieu de démarrer n'importe quoi.

## Fichiers touchés

| Fichier | Nature |
|---|---|
| `JOUER-SERVEUR.bat` | nouveau |
| `Fusion/marvel-lcg-src/launcher-serveur.sh` | nouveau |
| `Fusion/marvel-lcg-src/tools/test_serveur_multi.py` | nouveau |
| `.gitignore` | ajout de `.serveur/`, des dossiers `deck/serveur-*/` et `replays/serveur-*/` |

Aucun fichier du moteur n'est modifié.
