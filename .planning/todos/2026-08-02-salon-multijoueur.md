# TODO / SPEC — Salon multijoueur : chaque invité choisit son héros et son deck

**Statut :** ✅ **TERMINÉ.** Implémenté le 2026-08-03, et **la partie de test à deux a été
jouée : l'utilisateur l'a validée le 13/08/2026.** (Ancien texte : la partie de test à deux navigateurs (tâche 5, étape 5), qui ne peut pas être automatisée.
**Plan d'implémentation :** `.planning/plans/2026-08-02-salon-multijoueur.md` (5 tâches, prêt à dérouler tel quel)
**Date de conception :** 2026-08-02
**Origine :** demande utilisateur (« à quel point ça serait compliqué, pour quand on lance le multi, de laisser le choix aux invités de choisir leur perso et leur deck ? »)
**Écarts constatés pendant l'implémentation :**
- `launcher-multi.sh` n'existe QUE dans le dossier projet Windows, pas dans la copie WSL : la mise en garde « éditer les deux copies » ne s'appliquait pas.
- Le dépôt git ne suit pas le moteur (`Fusion/` entier est hors versionnement) : les étapes « commit » par tâche n'ont pas pu s'appliquer aux fichiers moteur.
- Les étapes 1 et 2 du wizard exigeaient que TOUS les joueurs aient un héros : en multi l'hôte serait resté bloqué sur l'écran des héros. Elles ne regardent plus que son propre siège ; c'est le LANCEMENT qui attend tout le monde.
- Un défaut introduit puis corrigé : le sondage calculait « il manque le Joueur 2 » même hors multi, ce qui grisait le bouton de lancement en solo hot-seat à deux. Garde-fou ajouté et couvert par `tools/test_salon.py ... solo`.
**Rapport à la roadmap :** indépendant. Ne remplace pas le serveur permanent spécifié dans `2026-07-28-serveur-permanent-multijoueur.md` — c'est le confort immédiat du mode « une soirée entre potes ».

---

## 1. Le problème

En multi, l'hôte assemble TOUT : scénario, difficulté, et le héros + le deck de chaque joueur. Les invités ne font que prendre un siège et attendre. Concrètement, il faut leur demander leur choix sur Discord, puis le saisir soi-même.

On veut que chaque invité choisisse son héros et son deck depuis son siège, et que l'hôte voie les choix arriver.

## 2. Ce qui existe déjà (vérifié le 2/8/2026)

C'est la partie la plus importante de cette spec : **la brique difficile est déjà là.**

- **Identité par siège.** `/claim_seat?p=N&key=MOTDEPASSE` pose un cookie `seat_token_<N>` (1 an) et redirige. `SEAT_PASSWORDS` (`launch.online.json`) donne un mot de passe par siège. `server_base.py` sait déjà vérifier qu'un client possède le jeton de SON siège. Un invité ne peut pas agir à la place d'un autre.
- **Le paramètre `to=`** de `/claim_seat` route déjà l'hôte vers `/prepare.html` et les invités vers `/app/board.html?p=N`. Ajouter une destination coûte une ligne.
- **Un précédent d'état partagé côté serveur** : `POST /set_cursor` + `GET /get_cursors` (`server_get.py`, 17 lignes). Un dict en mémoire, écrit par les clients, lu par les autres. C'est exactement la forme d'un salon.
- **`buildDescriptor()`** (`public/js/prepare/launcher.js`) construit `hero_json` à partir de `state.players[i].deck`. Si le salon remplit ce tableau, **le chemin de lancement ne change pas**.
- **Les decks sont déjà partagés.** `POST /save_deck` écrit dans `deck/custom/`, `GET /list_deck` les liste, et `catalog.decksForHero()` les propose sous « Sauvegardé ». Un invité peut donc DÉJÀ construire un deck via le tunnel et le rendre visible à l'hôte — il manque seulement de pouvoir le revendiquer pour son siège.
- **Les invités tolèrent de se connecter avant que la partie existe** : le plateau affiche un état d'attente.
- **La couche données est commune** : `catalog.js`, `api.js`, `cards.js`, `heros-info.js` sont des modules ES servis depuis `/public/js/prepare/`, utilisables par n'importe quelle page.

## 3. Décisions prises

| Question | Décision | Pourquoi |
|---|---|---|
| Un siège n'a pas choisi au moment de lancer | **Lancement bloqué**, avec la liste de qui manque | L'utilisateur préfère savoir qui on attend plutôt que de dépanner à la main |
| Comment savoir qui on attend | **L'hôte fixe le nombre de joueurs** (2/3/4) comme aujourd'hui ; on attend les sièges 2..N | Rien à tracer côté serveur, pas de gestion de présence ni de déconnexion |
| Réglage « premier joueur » | **Grisé en multi**, avec explication | `buildDescriptor` fait TOURNER l'ordre des joueurs pour l'appliquer, ce qui décollerait les sièges des personnes (voir §6) |
| Où l'invité choisit | **Page dédiée `/salon.html`** | Laisse `app.js` (1850 lignes, chemin solo quotidien) intact. Voir §4 |
| Ce que l'invité peut choisir | Héros + deck **parmi ceux déjà disponibles** : deck de base, packages d'aspect, decks sauvegardés | Périmètre « salon simple ». Pas d'import marvelcdb ni de deck-builder dans le salon |
| L'hôte choisit-il son propre héros dans le salon ? | **Non**, il garde son sélecteur du wizard (siège 1) | Il est déjà sur `/prepare.html`, l'y renvoyer serait un détour |
| Changement d'avis | **Autorisé** tant que la partie n'est pas lancée | Le dernier choix reçu écrase le précédent |

## 4. Approche retenue, et les deux écartées

**Retenue — page salon dédiée `/salon.html` + 2 routes serveur.** Une petite page autonome qui réutilise les modules de données déjà partagés. Le wizard n'apprend qu'une chose : afficher les choix reçus et bloquer le lancement.

*Écartée — réutiliser `/prepare.html` en mode « siège restreint »* (l'invité ouvre le wizard avec `?siege=2`, qui masque les étapes scénario/difficulté). Zéro duplication et l'invité aurait le sélecteur complet, mais cela ajoute un mode à un fichier de 1850 lignes : l'état global, la machine à étapes, la validation et le bouton de lancement devraient tous le connaître. Le risque de régression retombe sur le chemin SOLO, celui qui sert tous les jours.

*Écartée — extraire d'abord le sélecteur héros+deck dans un module commun.* Le plus propre à long terme, mais c'est une refacto d'`app.js` que personne n'a demandée, et le risque atterrit encore sur le solo (règle CLAUDE.md : ne pas réécrire ce qui marche sans demande explicite).

Le coût de l'approche retenue est une duplication **bornée** : une grille de héros et une liste de decks. Aucune logique de règles n'est dupliquée, la couche données étant commune.

## 4 bis. Numérotation des sièges — à ne pas confondre

Deux numérotations coexistent dans le code actuel, et les mélanger est le moyen le plus sûr de donner le deck du voisin à quelqu'un :

| | Hôte | Invités |
|---|---|---|
| Index technique `p=` (URL, cookie `seat_token_<p>`, index moteur) | **0** | 1, 2, 3 |
| Libellé affiché (lanceur, salon, wizard) | **Joueur 1** | Joueur 2, 3, 4 |

Dans toute cette spec, « siège 2..N » désigne les **libellés affichés**, donc les index `p=1..N-1`. Les clés du dict serveur et le corps de `POST /set_choix_siege` utilisent l'**index technique**.

## 5. Architecture

```
launcher-multi.sh          Joueur 2 : …/claim_seat?p=1&key=…&to=salon
                                                              ^^^^^^^ nouveau
        │
        ▼
/claim_seat  ── pose le cookie seat_token_1 ──▶  /salon.html?p=1
                                                      │
                        choisit héros + deck          │ POST /set_choix_siege
                                                      ▼
                                          état SALON en mémoire (serveur)
                                                      │
        /prepare.html (hôte) ── GET /get_choix_sieges ┘  sondage toutes les 2 s
                    │
                    └─ « Lancer » actif quand les sièges 2..N ont choisi
                       → buildDescriptor INCHANGÉ → /new → plateau
```

### 5.1 État serveur — deux routes dans `server_get.py`

Calquées sur `set_cursor` / `get_cursors`.

- **`POST /set_choix_siege`** — corps `{p, hero_card_id, deck_id, deck_source}`.
  On ne stocke **pas** le deck complet, seulement de quoi le retrouver : l'hôte le recharge par les routes existantes. Évite de faire transiter un JSON de 40 cartes et supprime tout risque de désynchronisation entre les deux copies.
- **`GET /get_choix_sieges`** — rend `{multi: bool, sieges: {"1": {...}, "2": {...}}}`.
  `multi` vaut vrai quand `SEAT_PASSWORDS` est non vide : c'est ce drapeau qui dira au wizard de griser « premier joueur » et d'activer le blocage du lancement.

Stockage : un dict en mémoire sur l'instance serveur, **sans péremption** (les curseurs périment à 5 s, pas le salon). **Vidé à la création de partie** (`/new`) pour que la partie suivante reparte propre.

Sécurité : l'écriture vérifie que l'appelant possède le cookie `seat_token_<p>` du siège revendiqué, via le mécanisme de `server_base.py`. Sans cette vérification, un spectateur ayant le mot de passe d'entrée pourrait changer le héros d'un joueur.

### 5.2 Page `/salon.html` (invité)

Trois écrans, un seul fichier JS d'environ 300 lignes plus un HTML.

1. **Attente / bienvenue** — « Tu es le Joueur 2 ». Si un choix existe déjà pour ce siège, il est rappelé et modifiable.
2. **Grille de héros** — construite depuis `catalog.heroes()`. Version simplifiée : vignette, nom, pas de recherche ni de favoris (ce sont des conforts du wizard, hors périmètre).
3. **Liste de decks** — `catalog.decksForHero(hero)`, qui rend déjà le deck de base, les packages d'aspect et les decks sauvegardés côté serveur. Un bouton valide et poste le choix.

Après validation, la page **sonde** : quand une partie existe, elle bascule sur `/app/board.html?p=N`. Détection par `GET /get_play_scene_name` (route existante) : elle rend le nom de la scène si une partie tourne, et une **chaîne vide** sinon. Réponse non vide = la partie est lancée, on redirige.

### 5.3 Côté hôte — `public/js/prepare/app.js`

Ajout **additif**, aucune fonction existante réécrite :

- Au chargement, appeler `/get_choix_sieges` ; si `multi` est faux, tout ce qui suit est inerte et le wizard se comporte exactement comme aujourd'hui.
- Sondage toutes les 2 s tant qu'on est sur l'étape des decks.
- À l'étape des decks, un siège **invité** (`p >= 1`) pour lequel un choix existe s'affiche **en lecture seule** (« Joueur 2 : Madame Web — Leadership+ ✓ ») et remplit `state.players[p]` (héros, deck, source). Un siège invité sans choix affiche « en attente ». Le siège de l'hôte (`p = 0`) garde son sélecteur local, en multi comme en solo : l'hôte ne poste jamais de choix au salon.
- Le bouton de lancement est bloqué tant qu'un siège 2..N n'a pas choisi, avec la liste des manquants.
- Le bloc « premier joueur » du panneau Avancé est grisé, avec une phrase d'explication.

### 5.4 `launcher-multi.sh` — ajout de `&to=salon`

Six lignes (les trois liens sont affichés deux fois : dans le message copié dans le presse-papier et dans l'encadré).

⚠️ **Ce fichier vit à la RACINE du moteur, hors du `rsync` du guide §1.3** : il faut l'éditer dans les DEUX copies (WSL et miroir), sinon le `.bat` de l'utilisateur continue de servir les anciens liens.

## 6. Le piège du « premier joueur »

`buildDescriptor()` fait pivoter la liste des joueurs pour placer le premier joueur en tête :

```js
const ordre = retenus.slice(pj).concat(retenus.slice(0, pj));
```

Le commentaire juste au-dessus dit « en multijoueur par sièges, le siège N correspond au joueur N ». Les deux ne peuvent pas être vrais en même temps : dès que `pj > 0`, le joueur assis au siège 2 se retrouve à piloter l'identité d'un autre.

En solo (hot-seat) le réglage reste utile et sans danger — l'hôte joue tout le monde. **Il n'est donc grisé qu'en multi**, pas supprimé.

## 7. Erreurs et cas limites

| Cas | Comportement attendu |
|---|---|
| Un invité ouvre `/salon.html` sans cookie de siège | Message « ouvre ton lien personnel », aucun choix possible |
| Un spectateur tente `POST /set_choix_siege` | 403 (vérification du jeton de siège) |
| Le serveur redémarre entre-temps | Le salon est vide, chacun rechoisit. Acceptable : le lien change aussi à chaque lancement |
| L'hôte réduit le nombre de joueurs de 4 à 3 | Le choix du siège 4 reste stocké mais n'est plus attendu ni utilisé |
| Un invité choisit un héros déjà pris par un autre | **Autorisé.** Le moteur accepte deux fois le même héros, et l'interdire demanderait une règle de plus. À revoir si ça gêne en vrai |
| Deux invités écrivent en même temps | Sièges différents, clés différentes dans le dict : pas de conflit |
| Un deck sauvegardé disparaît entre le choix et le lancement | L'hôte voit « deck introuvable » sur ce siège et le lancement reste bloqué |

## 8. Tests

Le multi ne se teste pas avec le harnais de cartes. Plan :

1. **Routes serveur** — script Python autonome, sur le modèle de `tools/test_newgame.py` : poser un choix, le relire, vérifier le refus sans jeton de siège, vérifier le vidage à `/new`.
2. **Logique de blocage** — la fonction qui décide « peut-on lancer » est pure : sièges attendus + choix reçus → booléen + liste des manquants. Elle est extraite dans son propre module et vérifiée par un script node, comme `outils/verifier-libelles-cible.mjs`.
3. **Bout en bout** — manuel, deux navigateurs, une partie à deux : c'est le seul moyen de valider la bascule salon → plateau.

## 9. Ce qui n'est PAS dans ce périmètre

- Import marvelcdb et deck-builder depuis le salon (l'invité peut toujours passer par `/deck-builder.html`, son deck apparaîtra dans la liste).
- Indicateur « prêt » distinct du choix.
- Fermeture de table / expulsion.
- Chat.
- Choix de l'identité alternative (The Thing Guardian) depuis le salon : reste au wizard de l'hôte.
- Tout ce qui relève du serveur permanent (lien fixe, plusieurs tables, secret des mains côté serveur) — voir `2026-07-28-serveur-permanent-multijoueur.md`.
