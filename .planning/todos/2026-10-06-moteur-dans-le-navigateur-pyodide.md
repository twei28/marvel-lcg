# Moteur dans le navigateur (Pyodide) : essai de faisabilité du 06/10/2026

**Statut : RÉALISÉ ET VÉRIFIÉ EN LOCAL (06/10/2026). NON DÉPLOYÉ, en attente du « déploie » de l'utilisateur. Le code vit dans `navigateur/` (voir la section « Produit » en bas de cette fiche). Rien n'est engagé, rien n'est déployé, aucun
fichier du moteur ni du serveur n'a été modifié.**

## Pourquoi
Le test de charge du 06/10 (voir `2026-09-16-tenir-plus-de-joueurs.md`) montre que le serveur ne tient
pas ~100 parties solo jouées en même temps (le CPU sature vers 25 à 40 tables). Les autres projets
(Warnel Chawpiovs, Digital Edition) n'ont pas ce problème parce que la partie tourne chez le joueur.
Demande de l'utilisateur : ne pas faire porter cette charge à son serveur.

## Ce qui a été fait
Le moteur (copie isolée dans le scratchpad, aucune écriture dans le dépôt) est lancé SANS navigateur ni
serveur dans Pyodide 0.27.8 (Python 3.12.7 compilé en WebAssembly), sous Node, avec le même amorçage
que `Fusion/marvel-lcg-src/tools/autoplay.py` (`Engine.Initialize`, `SceneLoader.NewFromJson`,
`GameSetup`, `GameLoop`). Partie : Spider-Man contre Rhino, graine 4321, pilote au hasard.

**Résultat identique au Python 3.10 natif : 29 questions, round 5** (même graine, même politique).
Le moteur se comporte donc pareil sous WebAssembly.

| Étape (archive chargée en mémoire, bytecode précompilé) | Pyodide | Python 3.10 natif |
|---|---|---|
| Démarrage de Pyodide | 2,7 s | n/a |
| Décompression du moteur (9,1 Mo zippé) | 1,3 à 1,6 s | n/a |
| Import du moteur | 1,1 à 1,3 s | 0,2 s |
| `Engine.Initialize` | 0,7 s | 0,3 s |
| `GameSetup` | 1,0 s | 0,3 s |
| `GameLoop` (partie complète) | 3,0 à 3,7 s | 1,7 s |

La boucle de jeu tourne ~1,8 à 2 fois plus lentement qu'en natif. Mémoire du processus : ~300 Mo.

**Poids à télécharger UNE fois (puis en cache du navigateur)** : Pyodide ~14 Mo (wasm 10 Mo + stdlib
2,4 Mo) + paquets (numpy 3 Mo, pillow 1 Mo, aiohttp et dépendances ~1 Mo) + moteur ~9 Mo (bytecode
inclus, données comprises) = **environ 28 Mo**. Comparable à une version web d'un jeu Godot.

## Ce qu'il a fallu contourner (et ce que ça apprend)
- **Paquets tiers du moteur** : `aiohttp`, `requests`, `typing_extensions`, `colorama`, `PIL`,
  `packaging`, `numpy`. Tous disponibles pour Pyodide (`colorama` en roue pure Python depuis PyPI).
- **Fils d'exécution** : Pyodide n'en a pas. `engine/job/manager.py` lance ses « jobs » dans un
  `ThreadPoolExecutor` ; remplacé POUR L'ESSAI par un exécuteur qui exécute tout de suite dans le même
  fil. Ça a suffi pour une partie solo complète. `engine/task/task.py` (vrai `threading.Thread`) n'a pas
  été atteint dans ce chemin.
- ⚠ **Piège de l'environnement, pas du moteur** : `node` tourne ici côté Windows (interop WSL). Il lit
  les fichiers WSL par le réseau (imports à 8,5 s au lieu de 1,1 s) et NE TRANSMET PAS les variables
  d'environnement sans `WSLENV` (comme pour Playwright). Un `FOO=1 node` silencieux = variable perdue.

## Ce que l'essai NE prouve PAS (le plus important)
1. **L'attente d'une réponse humaine.** Le moteur appelle `DeviceManager.DoGetInput` et BLOQUE jusqu'à
   la réponse. L'essai y branche un pilote qui répond tout de suite. Dans un navigateur il faut mettre
   le moteur dans un Web Worker et suspendre l'appel jusqu'au clic : soit `pyodide.ffi.run_sync`
   (JSPI, navigateurs récents), soit `Atomics.wait` sur un `SharedArrayBuffer` (exige les en-têtes
   COOP/COEP). Connu, non testé ici.
2. **Le plateau.** `ui-app` parle au moteur par ~60 routes HTTP et un WebSocket
   (`server_get.py`, `server_sync.py`, `server_socket.py`). Il faudrait un adaptateur qui répond à
   ces routes depuis le Worker (par exemple un Service Worker), ou réécrire la couche d'accès du plateau.
3. **Sauvegardes, campagnes, hauts faits, decks, replays** : fichiers côté serveur aujourd'hui, à
   renvoyer vers le stockage du navigateur (IndexedDB) ou vers le site pour les comptes.
4. **Un vrai navigateur** (Chrome, Firefox, mobile) : mesuré sous Node uniquement. Le WebAssembly y
   va à une vitesse du même ordre, pas identique. Le mobile est le point le plus incertain.
5. **Les ~5590 cartes** : une seule partie (Spider-Man, Rhino) a été jouée. Le chargement des cartes
   est paresseux ; tout le reste est à éprouver (le harnais `tools/test_capacites.py` pourrait servir).
6. **Le multijoueur en ligne** : hors périmètre, il garde besoin d'un serveur.

## Si on reprend (dans l'ordre)
1. Essai n°2 dans un vrai Chrome : moteur dans un Web Worker, une question humaine suspendue avec
   `run_sync` ou `Atomics.wait`, une partie jouée avec le plateau actuel branché sur un adaptateur
   minimal (quelques routes). C'est lui qui dit si l'idée vit.
2. Seulement ensuite : liste exacte des routes, stockage des sauvegardes, passage du harnais de cartes.

Fichiers de l'essai : `.planning/todos/pyodide-essai/spike_boot.py` (amorçage headless, commun
natif et Pyodide) et `run_pyodide.mjs` (chargeur Node). Les roues, le wasm et la copie du moteur
vivaient dans le scratchpad et ne sont pas conservés (les récupérer chez jsdelivr, Pyodide 0.27.8).


---

# Essai n°2 (06/10/2026, soir) : moteur dans un Web Worker d'un VRAI Chrome

Fichiers : `.planning/todos/pyodide-essai/chrome/` (`worker.js`, `boot_worker.py`, `index.html`,
`server.py` : un serveur statique avec les en-têtes COOP/COEP). Piloté avec Chrome DevTools, page servie
en local sur le port 8765 (arrêté ensuite, rien d'ouvert).

## Ce qui a marché
- **Le moteur BLOQUE bien sur la réponse de la page, sans geler la page.** `DoGetInput` appelle une
  fonction JS du Worker qui poste la question à la page puis fait `Atomics.wait` sur un
  `SharedArrayBuffer` ; la page écrit la réponse et fait `Atomics.notify`. Aucune modification du
  moteur : seulement le pilote branché dessus, comme `autoplay.py`.
- Page `crossOriginIsolated = true` (en-têtes `Cross-Origin-Opener-Policy: same-origin` et
  `Cross-Origin-Embedder-Policy: require-corp`).
- **509 questions humaines suspendues et reprises** en ~60 s, latence moyenne mesurée 155 à 156 ms
  pour une réponse volontairement retardée de 150 ms : **le surcoût de l'aller-retour est de ~5 ms**.
- **Le fil de la page reste libre** : son compteur de 100 ms a battu normalement pendant tout le
  calcul du moteur (1033 battements en ~105 s).
- Chargement à froid dans Chrome : Pyodide prêt en 3,1 s, moteur décompressé à 4,7 s, moteur
  initialisé 1,2 s plus tard, partie montée 1,9 s après le début du script Python. **~7 à 8 s avant
  la première question**, hors téléchargement (réseau local).

## Limites de cet essai (honnêtes)
- Le pilote d'essai ne termine jamais son tour (il tire une option au hasard, jamais « passer ») : la
  partie est restée au tour de Spider-Man, aucune fin de partie observée dans Chrome. Le moteur, lui,
  avait déjà terminé la même partie à l'essai n°1 (Node, 29 questions, round 5).
- **Le vrai plateau n'a PAS été branché.** Seul un écran d'essai minimal affiche les questions.
- Un seul navigateur (Chrome sur PC). Ni Firefox, ni Safari, ni mobile.
- Hébergement : COOP/COEP imposent de contrôler les en-têtes du serveur web (Caddy le permet ; un
  hébergement statique sans en-têtes personnalisés ne convient pas). Alternative sans ces en-têtes :
  `pyodide.ffi.run_sync` (JSPI), non essayé.

## Taille du dernier morceau : brancher le plateau actuel
Le plateau appelle une trentaine de routes (`/get_partie_en_cours`, `/get_ask`, `/post`,
`/client_updated`, `/get_world`, `/get_cards_json`, `/get_preferences`, `/save_preferences`,
`/get_campagne_en_cours`, `/manuel_*`, `/set_cursor`, `/sandbox_command`...) plus un WebSocket `/ws`.
Pour une partie solo, une dizaine suffisent ; les routes de salon, d'annonce, de rapport de bug et de
site peuvent répondre à vide. Pistes : un script injecté AVANT le plateau qui remplace `fetch` et
`WebSocket` par des appels au Worker (le plus court), ou un Service Worker pour `fetch` seul (le
WebSocket ne s'intercepte pas). Les handlers du moteur sont des méthodes `aiohttp` : à réutiliser tels
quels avec des requêtes factices (`aiohttp.test_utils.make_mocked_request`) plutôt que de réécrire les
réponses. Non essayé.

## Prochaine étape si on continue
Essai n°3 : brancher le plateau actuel (`/app/board.html`) sur le Worker avec le script injecté, jouer
un tour complet à la souris, relever ce qui manque. C'est lui qui dira si le produit est réaliste.


---

# Essai n°3 (06/10/2026, nuit) : le VRAI plateau sur le moteur du navigateur

Fichiers : `.planning/todos/pyodide-essai/plateau/` (`boot_navigateur.py` = l'adaptateur, `shim.js`,
`moteur-worker.js`, `server.py`). Page : le `public/app/board.html` EXISTANT (bundle construit, copie
dans le scratchpad) avec UNE ligne ajoutée (`<script src="/shim.js">`). Aucune modification du moteur,
du plateau ni du serveur.

## Ce qui a été joué, à la souris, dans un vrai Chrome, sans aucun serveur de jeu
Mulligan (« Garder ma main ») → tour de Peter Parker → « Fin du tour » → défausse de fin de tour →
**phase du méchant complète, pas à pas** (menaces +1 puis +3, activation de Rhino, sbires, cartes
rencontre, bilan ; « Ruée » tirée, manigance « L'Effraction ! » à 4/7, « Casser et Emporter » en jeu) →
**round 2, tour de Peter Parker**. 392 requêtes au total : toutes absorbées par le Worker. **Aucune
erreur** relevée dans le journal du moteur. Clic « Garder ma main » → plateau mis à jour : **107 ms**.

## Comment ça marche (la partie qui compte)
1. **Les VRAIES routes du moteur sont réutilisées, pas réécrites.** `GameServer(manager)` est instancié
   SANS jamais appeler `Run()` (aucun port), et chaque requête du plateau est servie en résolvant la route
   dans son `web_app` avec une fausse requête aiohttp (`faire_requete`, copiée de la logique de
   `aiohttp.test_utils`, absent du paquet Pyodide). Les ~60 routes (monde, question, réponse, cartes,
   préférences, sauvegardes...) répondent donc comme sur le serveur, y compris le masquage par siège.
2. **Les trames (WebSocket) viennent du vrai `WebSendRender`** ; `FauxWS.send_json` les poste à la page.
   Le moteur attend l'accusé de chaque trame comme d'habitude : le rythme pas à pas de la phase du
   méchant est celui d'aujourd'hui.
3. **Les attentes du moteur (`Condition.Wait`) traitent le courrier de la page** (au lieu d'attendre un
   autre fil), puis ne ré-évaluent leur condition QU'APRÈS une notification de CETTE condition, comme
   `wait_for`. ⚠ PIÈGE TROUVÉ : réveiller sur chaque message, ou sur toute notification, fait tourner le
   moteur en boucle (~260 requêtes par seconde, trames renvoyées sans fin) ; avec des réveils par
   condition, le trafic au repos tombe à ~0,25 requête par seconde.
4. **Le courrier page → moteur passe par un anneau en `SharedArrayBuffer`** (le Worker est bloqué dans
   `Atomics.wait` pendant que le moteur attend) ; moteur → page par `postMessage`.
5. Le plateau n'est modifié en rien : `fetch` et `WebSocket` sont remplacés AVANT son chargement.

## Ce qu'il reste à faire pour en faire un produit (non fait)
- **Créer une partie depuis l'assistant** (`prepare.html` → `/new`) : le handler `new_game` lance la
  partie dans un FIL (`game.NewGame`). Ici la partie est montée à la main au démarrage du Worker
  (Spider-Man contre Rhino, graine fixe). À faire : attendre le message `/new` dans le Worker puis monter
  et jouer la partie en ligne, et revenir à l'attente à la fin.
- **Images des cartes** : non copiées dans l'essai, le plateau affiche les noms. En vrai : soit les scans
  servis par le site (statique, cacheable), soit les CDN d'image déjà prévus par le moteur.
- **Sauvegardes, replays, hauts faits, campagnes, decks** : le moteur écrit des fichiers (`/eng` est en
  mémoire, perdu au rechargement). À brancher sur IndexedDB, ou sur le site pour les comptes.
- **Annuler** (`/debug?/undo`), le mode manuel, les pauses, la console : routes présentes mais pas jouées.
- **Autres cartes, autres héros, campagnes** : une seule partie jouée sur un round. Le harnais de cartes
  (`tools/test_capacites.py`) et `autoplay.py` sont les bons outils pour éprouver le reste, y compris sous
  Pyodide.
- **Navigateurs** : Chrome seulement. COOP/COEP exigent des en-têtes serveur (`credentialless` ici, absent
  de Safari ; sinon `require-corp` avec des images en CORP). Mobile non essayé : c'est le risque principal.
- **Poids et démarrage** : ~28 Mo une fois, puis ~4,5 s de démarrage de Pyodide et du moteur + la montée
  de la partie. À présenter derrière un écran de chargement.
- **Multijoueur en ligne** : toujours besoin d'un serveur, hors de ce chantier.

## Correction apportée aux évaluations précédentes
Le plateau n'appelle pas ~60 routes à réécrire : l'adaptateur réutilise les routes du moteur telles
quelles. Le « dernier morceau » est donc nettement plus petit que prévu à l'essai n°2.


---

# Produit : `navigateur/` (06/10/2026, nuit)

**Le jeu tourne entièrement dans le navigateur.** Moteur et plateau INCHANGÉS ; tout est dans `navigateur/` :

| Fichier | Rôle |
|---|---|
| `construire.py` | assemble `navigateur/dist` (Pyodide 0.27.8, roues, moteur en bytecode, pages et plateau de `public/`) ; `--sans-pages` pour ne refaire que le moteur et les scripts. Ne reconstruit PAS le plateau (`bash ui-app/deployer.sh` avant si ui-app a changé). |
| `src/navigateur.html` | la COQUILLE : tient le Worker et IndexedDB, ne se recharge jamais ; le jeu vit dans un `<iframe>` (changer de page ne tue plus le moteur). Écran de chargement. |
| `src/shim.js` | injecté en tête de chaque page : redirige `fetch`, `XMLHttpRequest` (runtime historique) et `WebSocket` vers le moteur. |
| `src/moteur-worker.js` | Worker : Pyodide, restauration des fichiers du joueur, courrier par anneau `SharedArrayBuffer`. |
| `src/boot_navigateur.py` | l'adaptateur : vrai `GameServer` sans port, fausses requêtes aiohttp, attentes du moteur qui traitent le courrier, vraie boucle `Engine.EngineRun()`, synchro `/eng/persist` vers la page. |
| `serveur-local.py` | serveur statique d'essai (mêmes en-têtes COOP/COEP, scans redressés comme le moteur). |
| `preparer-scans.py` | écrit les versions tournées des 2947 scans paysage (sur 21 479) pour un hébergement statique. |
| `Caddyfile.exemple` | exemple d'hébergement (non déployé). |
| `essais/` | banc d'équivalence moteur normal / navigateur (`equivalence.py`). |

## Vérifié (en local, Chrome)
- **60 parties sur 60 IDENTIQUES** entre le moteur normal (Python 3.10) et celui du navigateur (Pyodide,
  Python 3.12) : mêmes questions, même round, même issue, mêmes PV du vilain. Héros tirés au hasard dans les
  139 decks de départ (officiels, vagues, fan-made), vilains tirés parmi 190 scénarios, graines tirées.
  Détail : `navigateur/essais/resultats-equivalence.json`. Relancer : `python3 navigateur/essais/equivalence.py 60 2026`.
- **Parcours réel à la souris** : assistant « Préparation de mission » (69 héros) → Solo → Spider-Man → decks → Rhino →
  Lancer la partie → plateau avec les vrais scans français → mise en place, mulligan, fin de tour, phase du
  méchant → round 2. **Annuler** (retour au mulligan), **Sauver**, **Reprendre** après rechargement de la page
  (la liste affiche « Spider-Man, Rhino, pas 2 » et la partie revient au bon tour).
- **Sauvegardes** : tout ce que le moteur écrit sous `./persist` part vers IndexedDB (le Worker est bloqué,
  IDBFS est inutilisable) et revient au démarrage suivant.
- **Pages parcourues sans erreur du moteur** : éditeur de deck, cartes, galerie, campagnes, hauts faits,
  crédits, palettes, bac à sable.

## Défauts trouvés et corrigés en route (pour mémoire)
1. Écran « Loading » infini : promesse IndexedDB jamais résolue (deux requêtes chaînées).
2. Plateau vide puis emballement (~260 requêtes/s) : les attentes du moteur doivent se réveiller par CONDITION et
   sur notification seulement ; et le moteur doit être notifié à la connexion du WebSocket.
3. Scripts en 404 : le moteur sert `public/` sous `/public/` ET à la racine ; le build réécrit `/public/` en `/`.
4. **Manigance couchée** (signalé par l'utilisateur : « le jeu normal ne le fait pas ») : le moteur redresse EN PORTRAIT
   tout scan plus large que haut (`engine/file/cache.py`, `TryRotateImage`) et le plateau le remet à plat par CSS ;
   un serveur de fichiers bruts les couche. D'où `preparer-scans.py` et la rotation du serveur d'essai.
5. « Reprendre » en erreur : le moteur ne sait pas retrouver un chemin ABSOLU POSIX dans ses dossiers de
   sauvegarde (`FileManager.FindJsonPath` joint `./` + chemin) ; les chemins sont donc relatifs (`./persist/...`).
6. L'ancien menu `main.html` (« Digital Edition », jeu d'origine d'irefrixs) n'est pas l'entrée : la coquille ouvre `/prepare.html`.

## Limites connues (non traitées)
- **Navigateurs** : essayé dans Chrome seulement. Firefox et Safari non testés ; `credentialless` (COEP) n'existe pas
  dans Safari ; mobile non essayé (mémoire du moteur ~300 Mo, démarrage ~5 s sur PC).
- **Hébergement** : exige les en-têtes COOP/COEP sur toutes les réponses (voir `Caddyfile.exemple`) ; les scans doivent
  être servis redressés (`preparer-scans.py`) ; le moteur ne va PAS chercher en ligne les images absentes des
  dossiers d'assets (ton serveur le fait via `image_servers`) : ces cartes s'affichent avec leur seul nom.
- **Poids** : ~28 Mo à télécharger une fois (Pyodide 14 Mo, paquets 5 Mo, moteur 9 Mo) + `public/` ; scans à part.
- **Non éprouvé** : campagnes de bout en bout, Legacy, mode manuel/pause, replays « Revoir », import de decks
  MarvelCDB (appelle Internet), bataille/coop locale à plusieurs héros dans le navigateur. Le banc d'équivalence ne
  couvre que le solo en moteur seul (pilote au hasard).
- **Multijoueur en ligne** : hors périmètre (besoin d'un serveur).
- **La table du serveur et ce chantier ne se parlent pas** : les comptes, parties suivies et sauvegardes serveur ne
  sont pas branchés sur le mode navigateur (ses sauvegardes restent dans le navigateur du joueur).

## Pour publier (rien n'est fait)
1. `bash ui-app/deployer.sh` si le plateau a changé, puis `python3 navigateur/construire.py`.
2. `python3 navigateur/preparer-scans.py <dossier>` et déposer les scans redressés.
3. Servir `navigateur/dist` avec les en-têtes COOP/COEP (voir `Caddyfile.exemple`), ouvrir `/navigateur.html`.


---

# Mise en ligne sur `play.narwhalchampions.com` : décisions et état (06/10/2026, soir)

## Décisions de l'utilisateur (questions une à une)
- **Adresse** : `play.narwhalchampions.com` (sous-domaine, couvert par le certificat wildcard déjà en place).
- **SANS COMPTE** : on arrive directement sur l'assistant de choix du héros ; langue et affichage demandés la première
  fois et retenus dans le navigateur ; sauvegardes dans le navigateur (IndexedDB). Pas de lien avec le compte du site
  au lancement (possible plus tard : les sauvegardes sont de simples fichiers).
- **Public visé : les joueurs en général**, pas les joueurs de confiance : donc PAS de signalement de bug ni
  d'administration dans ce mode.
- **Perte de parties** : boutons « Exporter mes parties » / « Importer » + demande de stockage persistant au navigateur.
- **Discord** : laissé tel quel (le moteur ne peut sans doute pas tourner dans le cadre Discord : l'isolation exige que
  tous les cadres parents le soient ; non vérifiable sans client Discord). Un bouton « Je n'ai pas de compte » ouvrant
  play. dans le navigateur a été proposé puis écarté.
- **Mises à jour** : tout ce qui est fait pour la version avec compte (cartes, règles, plateau, traductions) entre dans le
  paquet navigateur, MAIS seulement après reconstruction et publication ; jamais automatiquement.
- **Ouverture** (publique d'emblée, ou adresse sans lien quelques jours) : NON TRANCHÉE.

## Fait en local (rien n'est en ligne)
- Bouton « Signaler un bug » retiré de l'écran de préparation (il est construit sans interroger le serveur) ; routes
  `/post_rapport_bug` (403), `/get_rapport_actif` (`{"actif":false}`), `/get_site_admin`, messages privés neutralisées.
- Export / import d'un fichier JSON (`marvel-champions-navigateur`), chemins validés (`/eng/persist/*.json` seulement) ;
  essai complet : navigateur vidé → import → « Reprendre » retrouve la partie sans recharger.
- `navigator.storage.persist()` demandé (Chrome peut refuser : il ne l'accorde qu'à un site assez fréquenté).
- Navigateur non pris en charge (WebAssembly, Worker, IndexedDB, SharedArrayBuffer/isolation) : message clair + lien vers
  les tables du serveur ; avertissement « expérimental » sur téléphone/tablette (continuer possible).
- Version = empreinte du contenu (`dist/version.json`) ; worker et moteur chargés avec `?v=<version>` ; bandeau
  « nouvelle version disponible » (la partie est sauvegardée automatiquement).
- `navigateur/publier.py` : construit, lance le CONTRÔLE D'ÉQUIVALENCE (arrêt à la moindre différence), puis rsync.
  SIMULATION par défaut ; `--oui` pour envoyer, uniquement après le « déploie ». Non branché sur `deployer.ps1`.
- `navigateur/Caddyfile.exemple` : le bloc `@play` à insérer dans le bloc wildcard du Caddyfile (en-têtes COOP/COEP
  limités à play., scans redressés d'abord, cache). `preparer-scans.py` écrit `<sortie>/pivotes/<dossier>/`.

## Reste à faire (avec le « déploie »)
1. Créer `/opt/narwhal-play` et `/opt/narwhal-play-scans/{pivotes,originaux}`, y poser les scans, insérer le bloc Caddy,
   `systemctl reload caddy`. Vérifier que l'enregistrement DNS wildcard couvre `play.`.
2. `python3 navigateur/publier.py --oui`.
3. Essayer sur Firefox, Safari, mobile (jamais testés), et trancher l'ouverture.
4. Brancher `publier.py` sur la commande de déploiement habituelle (non fait : `deployer.ps1` est partagé avec d'autres chantiers).


---

# Constat du contrôle d'équivalence (06/10/2026, nuit) : une instabilité RARE du moteur dans le navigateur

## Correction de ce qui était annoncé plus haut
Le « 60 parties sur 60 identiques » de la section « Produit » avait un écart de configuration : le moteur normal tournait
avec `statistics: false`, le paquet navigateur avec `statistics: true` (comme ton jeu). Les statistiques et hauts faits
enregistrent des effets de règle, donc changent les identifiants d'objets. Le banc utilise maintenant LA MÊME
configuration des deux côtés et un état VIERGE par partie native (les statistiques écrites d'un lancement à l'autre
faussaient aussi les comparaisons). Refait : **58 identiques sur 60**, les 2 écarts étant Conan et Invisible Woman.

## Ce qui a été établi
- **Le moteur normal est reproductible** (état vierge) : Conan contre Captain Marvel expert, graine 7368 → 22 questions,
  18 lancements sur 18, quel que soit `PYTHONHASHSEED` (0 à 9).
- **Le moteur du navigateur varie d'un lancement à l'autre sur certaines parties** : la même partie donne 22, 37 ou 41
  questions (Conan), ou 15 ou 14 (Invisible Woman, 1 lancement sur 6). Les deux sont des héros à PLUSIEURS FORMES.
- **Premier point de divergence** : au tour du joueur, l'ORDRE des boutons « Change To Conan the Barbarian / the Thief »
  change (les options sont triées par `object_id` d'effet, `event/manager.py:305`, et ces identifiants varient). Un
  pilote qui choisit « le n-ième bouton » joue alors une autre partie. Pour un joueur humain, seul l'ordre des boutons
  change : la partie reste valide.
- Dans Pyodide, SANS réglage, l'ordre de hachage des chaînes ET les adresses mémoire (`id()`) changent à chaque
  lancement ; avec `loadPyodide({ env: { PYTHONHASHSEED: "0" } })` ils sont identiques d'un lancement à l'autre
  (vérifié sur `hash('abc')` et `id(object())`). Mais fixer ce paramètre n'a PAS suffi à rendre la partie de Conan stable :
  il existe au moins une autre source de variation, NON ISOLÉE.
- Un correctif de tri dans `game/player/element/player_setup.py` (`list(identities)` → liste triée) a été essayé sur une
  COPIE du paquet : insuffisant (la partie varie encore, 37 ou 41). Aucun fichier du moteur du dépôt n'a été modifié.

## Ce que ça veut dire
- **Jouer** : sans conséquence visible, au pire l'ordre de deux boutons.
- **RISQUE NON VÉRIFIÉ : « Reprendre » une partie sauvegardée** avec un héros à plusieurs formes. La reprise rejoue les
  réponses enregistrées par identifiant d'option ; si ces identifiants changent d'un lancement à l'autre, la reprise
  pourrait se désynchroniser. Vérifié seulement avec Spider-Man (un seul héros, une seule forme) : OK.
- **Le contrôle de publication** (`navigateur/publier.py`) rejoue maintenant une partie qui diffère jusqu'à 5 fois et ne
  la retient comme RÉELLE que si aucun lancement ne retrouve le résultat du moteur normal ; une instabilité connue est
  signalée « INSTABLE » sans bloquer.

## À faire (par ordre d'intérêt)
1. Tester « Reprendre » sur Conan et Invisible Woman dans le navigateur (jouer quelques actions, recharger, reprendre).
2. Isoler la seconde source de variation (comparer les journaux d'allocation d'objets de deux lancements qui divergent) ;
   pistes : ordre d'enregistrement des effets d'un héros à plusieurs formes, ensembles d'objets hachés par adresse.
3. Régler `PYTHONHASHSEED=0` dans le Worker (déjà utile : adresses reproductibles) une fois la cause trouvée.


---

# Instabilité des héros à plusieurs formes : CAUSE TROUVÉE ET CORRIGÉE (07/10/2026)

## La cause (dans le moteur, pas dans Pyodide)
`game/player/element/player_setup.py`, `register_change_form` : les formes d'un héros (Conan : cn001a à cn001e) sont les FACES
d'UNE SEULE carte. `sorted(identities)` compare `card.object_id` (`CardFace.__lt__`), donc des clés TOUTES ÉGALES : le tri ne
départageait rien et gardait l'ordre d'itération d'un `set` d'objets hachés par adresse mémoire. L'ordre d'enregistrement des
capacités « Change To … », donc leurs `object_id`, donc l'ORDRE DES BOUTONS (`event/manager.py:305` trie les options par
`object_id`) variait d'un processus à l'autre. Le moteur normal le cachait par hasard (disposition mémoire stable) ; dans
Pyodide les adresses changent à chaque lancement : trois issues pour une même graine (Conan), deux pour Invisible Woman.
Mes essais précédents sur cette piste (« tri simple », `PYTHONHASHSEED`) échouaient parce que le tri restait à égalité, et
mes comparaisons étaient brouillées par des fichiers de statistiques gardés d'un lancement à l'autre.

## Le correctif (2 lignes, `player_setup.py`)
`identities_triees = sorted(identities, key=lambda x: (x.card.object_id, x.paper.card_id))`, utilisée à la fois pour la
boucle et pour la liste des « autres formes ». `paper.card_id` départage deux faces de la même carte, de façon stable.

## Vérifié
- Les trois parties instables (Conan ×2, Invisible Woman) : **10 lancements sur 10 identiques dans le navigateur, 3 sur 3 en
  natif, et identiques entre eux.**
- **Anciennes sauvegardes : pas de risque.** La reprise ne retrouve pas une action par son identifiant brut mais par la CARTE et
  le NOM de la capacité (`game/scene/replay/operation.py`, `FindNewEffectId`). Le correctif change pourtant l'identifiant de
  « Change Form » pour **52 héros sur 139** au premier tour (le plus souvent 7 → 8) : sans conséquence pour la reprise.
- **« Reprendre » avec Conan dans le navigateur**, par la vraie interface : changement de forme vers Barbarian, sauvegarde,
  rechargement complet de la page, reprise → Conan the Barbarian, 6 cartes en main, round 1, aucune erreur.


---

# ✅ DÉPLOYÉ le 07/10/2026 : `https://play.narwhalchampions.com`

Sur « Les deux » puis « Déploie maintenant, tel quel » de l'utilisateur (son autre session travaillait encore sur le plateau :
`board.tsx`, `Board.tsx`, `test_capacites.py` modifiés à 09:43 et 09:58 ; le plateau construit `board-vm1FWojQ.js` de 09:38 est
parti avec). Trois commits sur la branche `mode-manuel` : `9937458b` (correctif moteur), `2d5e8e48` (navigateur/), `72792d29` (docs).

## 1. Le jeu (serveur actuel) : `deployer.ps1 -Code`
Service `narwhal` actif, `https://narwhalchampions.com/` HTTP 200, correctif présent sur le serveur (3 occurrences de
`identities_triees`), bundle en ligne identique au local (`board-vm1FWojQ.js`). Le serveur de jeu a redémarré (parties en cours perdues).

## 2. Le mode navigateur : `python3 navigateur/publier.py --oui`
Construction (version `29ade4bb1b`), contrôle d'équivalence **20 parties sur 20 identiques**, `rsync` vers `/opt/narwhal-play` (82 Mo).

## 3. Ce qui a été fait À LA MAIN sur le serveur (hors du dépôt, à connaître)
- **`/etc/caddy/Caddyfile`** (jamais écrasé par `deployer.ps1`, il importe karaoke et publicverse) : bloc `@play host play.{$DOMAINE}`
  inséré avant `@p1` dans le bloc wildcard, puis les routes `/scan/*` et `/vignette/*`, puis les textures `.webp`. Trois sauvegardes :
  `/etc/caddy/Caddyfile.avant-play-20261007`, `...avant-vignettes-20261007`, `...avant-textures-20261007`. Chaque modification a été
  validée (`caddy validate`, avec `/etc/caddy/cloudflare.env` chargé) avant `systemctl reload caddy`.
- **`/opt/narwhal-play-scans/`** : `originaux/` = COPIE de `pics-fr`, `pics`, `textures`, `cache`, `vignettes` (1,9 Go) ; `pivotes/` =
  2947 scans paysage redressés (270 Mo), générés SUR le serveur par `preparer-scans.py` (venv du jeu, `nice 19`).
  ⚠ Pourquoi une copie et pas un lien : `/opt/narwhal` est en 750 `narwhal:narwhal`, Caddy (groupes `caddy`, `www-data`) ne peut pas le lire.
  Ne PAS ouvrir les droits de `/opt/narwhal` pour ça.
- DNS : rien à faire, le DNS générique `*.narwhalchampions.com` couvrait déjà `play.`.

## 4. Défauts trouvés au contrôle sur l'adresse en ligne, corrigés
- Miniatures de la table grises : le plateau demande aussi `/vignette/<id>` (le moteur sert la miniature, sinon le scan complet,
  `Cache.LoadVignette`) ; route absente, 404. Corrigé (route Caddy + copie du dossier `vignettes`).
- Dos génériques `player` / `encounter` : ils vivent dans `textures/` en `.webp`, extension absente de la liste. Corrigé.
- `preparer-scans.py` s'arrêtait sur un scan RGBA enregistré en JPEG : conversion en RGB, un échec n'arrête plus le lot.

## 5. Vérifié sur l'adresse en ligne (Chrome)
Page isolée, moteur prêt en 8 s, assistant, partie lancée, plateau, manigance à l'endroit, miniatures et dos affichés, scans et
miniatures en HTTP 200 sans échec, « Reprendre » après rechargement. En-têtes COOP/COEP présents, apex toujours à 200.

## 6. Pour redéployer le mode navigateur
`python3 navigateur/publier.py --oui` (construit, contrôle l'équivalence, envoie). Les scans et le Caddyfile ne changent que si de
nouveaux scans paysage apparaissent : relancer alors `preparer-scans.py` sur le serveur (voir ci-dessus).
## 7. Reste non fait
Firefox / Safari / mobile jamais testés ; ouverture publique non tranchée (l'adresse est joignable, SANS lien depuis le site) ;
`publier.py` pas branché sur `deployer.ps1`.
