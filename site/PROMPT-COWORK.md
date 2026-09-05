# Brief pour Claude Cowork — mise en ligne de NarwhalChampions

*Copie tout ce qui suit dans Cowork.*

---

Je veux mettre en ligne un site nommé **NarwhalChampions**. L'application est
déjà écrite et fonctionne : ton travail porte sur **le domaine, le serveur, le
DNS, le HTTPS et le déploiement**, pas sur le code applicatif.

## Ce qui existe déjà

Un moteur de jeu de cartes écrit en **Python 3.10**, qui **sert lui-même le
HTTP et le WebSocket** (aucun serveur web n'est nécessaire pour l'application
elle-même). Deux composants :

1. **Le moteur** (`Fusion/marvel-lcg-src/`), lancé par
   `python3.10 launcher_fast.py --config <fichier.json> --no-browser`.
   Il est **mono-partie** : une partie = un processus = un port.
2. **L'orchestrateur** (`site/orchestrateur.py`), déjà écrit, sans dépendance
   externe (bibliothèque standard seulement). Il écoute sur `127.0.0.1:8080`,
   affiche la page d'accueil, gère les comptes, et démarre/arrête un moteur par
   partie sur les ports **2351 à 2370** (20 tables).

## Chiffres mesurés (pas estimés)

- **69 Mo de RAM par partie**, réponse HTTP en 6 ms.
- 20 tables × 69 Mo = **1,4 Go**. Un VPS **4 Go** suffit largement.
- 20 tables × 4 joueurs = **80 joueurs simultanés** (plafond technique).
- **20 comptes** au maximum, plafond choisi par moi. ⚠ Ce n'est pas le même
  nombre que le précédent : un compte n'est nécessaire que pour **ouvrir** une
  table, les trois autres joueurs arrivent par un lien de siège sans compte.
- Le dossier d'images fait **2,3 Go pour 5893 fichiers**, mais :
  - **4474 images officielles** sont déjà téléchargées en ligne par le moteur
    (clé `image_servers` de `launch.json`, qui pointe sur Cerebro et
    MarvelCDB) : **rien à copier pour elles** ;
  - **1419 images custom pèsent 1,9 Go** et doivent, elles, être copiées.
    Elles sont en 1500×2150. Un redimensionnement vers ~800 px de large les
    ramènerait autour de 200 Mo : à faire si le transfert pose problème.
  - ⚠ **`assets/pics/` est dans le `.gitignore`** : ces images ne sont pas
    dans le dépôt, elles doivent voyager par `rsync`.

## ⚠ La contrainte qui détermine toute l'architecture

**Un sous-domaine par partie, jamais un préfixe de chemin.**

Le client du jeu utilise des **chemins absolus** partout : `/ws`,
`/save_deck`, `/set_choix_siege`, `/app/board.html`, `/get_achievements`,
`/load_replay_data`… Servir une partie sous `narwhalchampions.xx/partie3/`
ferait repartir chacun de ces appels à la racine du site au lieu du moteur de
la partie, et tout casserait.

Il faut donc :

- `narwhalchampions.xx` → l'orchestrateur (`127.0.0.1:8080`)
- `p1.narwhalchampions.xx` → `127.0.0.1:2351`
- `p2.narwhalchampions.xx` → `127.0.0.1:2352`
- … jusqu'à `p20.narwhalchampions.xx` → `127.0.0.1:2370`

Ces **20 routes sont statiques** : déclare-les une fois pour toutes. C'est
l'orchestrateur qui alloue dynamiquement les tables, le routage ne bouge
jamais. Ne mets pas en place de reconfiguration de Caddy en vol.

Le **WebSocket** (`/ws`) doit passer sur les sous-domaines `p1`…`p20`.

## Ce que je te demande de livrer

1. **Le choix et l'achat du domaine** `narwhalchampions` (propose-moi les
   extensions disponibles et leur prix ; je paie).
2. **Le choix du VPS** : 4 Go de RAM minimum, Linux, autour de 5 €/mois.
   Propose deux options chiffrées, je paie.
3. **Le DNS** : un enregistrement A sur l'apex, et un enregistrement
   **wildcard `*.narwhalchampions.xx`** vers la même IP.
4. **Caddy** en frontal, avec :
   - un **certificat wildcard**, ce qui impose un **challenge DNS** (donc un
     jeton API chez le fournisseur DNS ; Cloudflare le fait gratuitement) ;
   - les 20 routes statiques ci-dessus plus l'apex ;
   - le WebSocket qui passe.
5. **Un service systemd** pour l'orchestrateur, qui redémarre tout seul.
   Il doit connaître trois variables d'environnement :
   `RACINE_JEU` (chemin du moteur), `PYTHON` (chemin du Python 3.10),
   `DOMAINE` (`narwhalchampions.xx`, sert à fabriquer les liens affichés).
6. **Un script de déploiement** que je relance à chaque mise à jour : il
   pousse le code **et** les images custom par `rsync`, puis redémarre le
   service. Le dépôt seul ne suffit pas, les images n'y sont pas.
7. **Le pare-feu** : seuls 80 et 443 ouverts. Les ports 2351-2370 et 8080 ne
   doivent **jamais** être joignables de l'extérieur, Caddy est le seul point
   d'entrée.
8. **Un mode d'emploi en français**, court, que je puisse suivre seul : mettre
   à jour, redémarrer, lire les journaux, restaurer.

## Points d'attention

- **Python 3.10 précisément** est requis par le moteur.
- L'orchestrateur tue les moteurs par **groupe de processus** : ne l'exécute
  pas dans un conteneur qui l'en empêcherait sans le tester.
- Chaque table écrit dans ses propres dossiers (sauvegardes, decks, campagnes,
  statistiques). Prévois de la place disque et une purge.
- **Comptes** : le site a sa propre inscription avec **validation manuelle par
  moi**, plafonnée à **20 comptes**. C'est l'orchestrateur qui la gère, tu n'as
  rien à coder pour ça — mais **ne mets aucune authentification Cloudflare
  Access par-dessus** : elle ferait doublon, et surtout elle bloquerait les
  invités, qui doivent pouvoir rejoindre par leur lien de siège **sans
  compte**. Les sous-domaines `p1` à `p20` doivent rester librement joignables :
  ils sont protégés par les clés de siège du moteur, pas par le site.
  Les variables d'environnement du service sont `MAX_COMPTES=20`,
  `ADMIN=<mon pseudo>` et `FICHIER_COMPTES=<chemin>`.
- Le fichier des comptes doit être **sauvegardé** : c'est la seule donnée du
  site qui ne se régénère pas.

## Questions à me poser avant d'acheter quoi que ce soit

Le prix final, l'extension de domaine retenue, et l'hébergeur. Je veux valider
avant tout engagement.
