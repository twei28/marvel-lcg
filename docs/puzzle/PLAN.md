# Puzzles : plan d'implémentation (22/10/2026)

Complète `CAHIER-DES-CHARGES.md`. Aucun code écrit. Une seule livraison, mais
construite dans cet ordre (chaque étape testable seule).

## Ce qui existe déjà (à réutiliser)
- **Moteur** : `src/game/puzzle/` (`PuzzleData`, `RunPuzzle` avec ~80 commandes
  `Puzzle.*` : Damage, Stun, Exhaust, MoveTo, Attach, PutIntoPlay, Win, Lose, End…).
  7 puzzles officiels dans `Fusion/marvel-lcg-src/puzzle/*.json`, avec checksum.
- **Routes serveur** : `/list_puzzle_files`, `/get_puzzle_json`, `/load_puzzle`,
  `/new_puzzle`, `/new_puzzle_replay` (`server_new_game.py`, `server_get.py`).
- **Interface** : `navigateur/dist/js/prepare/puzzles.js` (liste + chargement),
  `puzzle_editor.html` (ancien éditeur texte), et surtout le **bac à sable**
  (`js/sandbox/app.js`) : un panneau avec catalogue de cartes qui pilote la partie en
  cours via `POST /sandbox_command` (commandes `Puzzle.*`, seules autorisées).
- **Replays** : le moteur sait déjà rejouer une partie (`is_puzzle`).

## Constats qui pèsent sur le plan
1. `play_puzzle` ne met en place que `players[0]` (main, deck, défausse) : le
   **multi-héros (1 à 4)** demande d'étendre moteur et format.
2. Il n'existe pas de commande pour : premier joueur, ressources en réserve, phase
   de départ, stade du méchant, objectifs. À ajouter.
3. Il manque l'inverse de tout ça : **capturer l'état du plateau** et le convertir
   en puzzle. C'est la plus grosse pièce.
4. Un puzzle publié exécute des commandes sur la machine d'autres joueurs :
   il faut une **liste blanche stricte** (déjà `Puzzle.<méthode>` seulement).
5. Deux déploiements : serveur (Python) et navigateur (Pyodide, `navigateur/`).
   Toute nouveauté moteur doit passer le contrôle d'équivalence.
6. Le moteur existe en plusieurs copies : lire `GUIDE-CREATION-CONTENU.md` §1 avant
   de toucher quoi que ce soit dans `Fusion/`.

## Étapes

### E0. Cadrage — FAIT (22/10)
- Lire GUIDE §1, étudier `puzzle.py`, `puzzle_data.py`, le bac à sable et ses tests.
- Décider définitivement : étendre `PuzzleData` (version 2, compatible avec les 7
  puzzles existants, checksum conservé ou assoupli).

### E1. Format de puzzle v2 — FAIT (22/10), voir FORMAT-V2.md
Ajouter : titre, description, difficulté, indices, objectifs (ET/OU, cible du
complot), visibilité de la solution, solution de référence (replay), état détaillé
par héros (PV, forme, statuts, premier joueur, ressources), phase de départ,
auteur/pseudo. Migration des anciens fichiers. Validation de taille et de schéma.

### E2. Moteur : mise en place complète
- `play_puzzle` pour 1 à 4 héros.
- Nouvelles commandes `Puzzle.*` : premier joueur, ressources, phase/étape de départ,
  stade et PV du méchant, complot (étape, menace, accélération), mise en jeu avec
  dégâts/compteurs/statuts/attachements.
- Garder la liste blanche ; tests unitaires de chaque commande.

### E3. Moteur : objectifs et fin de puzzle — MOTEUR FAIT (23/10) ; écran de réussite (interface) à faire avec l'utilisateur
- Détection automatique : vaincre le méchant ce tour, survivre jusqu'à la fin du
  tour, terminer le complot ciblé, combinaisons ET/OU. Objectif libre : bouton manuel.
- Écran de réussite / d'échec (réutiliser les bannières Victoire/Défaite).
- Mode automatique forcé en puzzle.
- Fait : `src/game/puzzle/puzzle_objectives.py` ; objectifs portés par la scène (`puzzle_objectifs`,
  `puzzle_objectifs_mode`), exposés au client (`puzzle_objectives`). Règles : tous les objectifs
  (`all`) ou un seul (`any`) → victoire « Players Won » ; round fini sans les atteindre →
  défaite « The Puzzle Objectives were not Met » ; défaite du moteur (héros éliminés, complot
  principal achevé qui n'est pas la cible, deck de rencontre vide) reste une défaite. « Terminer
  le complot » : complot annexe = vaincu (menace à 0) ; complot principal = achevé (réussite,
  pas défaite). Objectif libre : `Puzzle.ValidateObjective(i)`. Sans objectif : fin du moteur
  inchangée. 13 cas dans `outils/test_puzzle_moteur.py` (lancer avec `~/.marvel-venv/bin/python`).
- Interface faite (23/10, choix de l'utilisateur) : panneau « Objectifs » repliable en haut à
  gauche, en orange (`ui-app/src/board/PanneauObjectifs.tsx`), case à cocher pour l'objectif
  libre (route dédiée `/puzzle_objectif`, jamais `/sandbox_command`), écran de fin = bannière
  Victoire/Défaite + bilan des objectifs (coche / croix). 7 tests vitest.
- Reste : boutons Rejouer / Voir la solution / Retour aux puzzles sur l'écran de fin (E7) ;
  la route `/puzzle_objectif` n'existe pas encore côté navigateur (Pyodide, `navigateur/`) :
  à reporter avec le contrôle d'équivalence ; aucune capture réelle du panneau en partie
  (écrit et testé en unitaire seulement).

### E4. Capture de l'état (cœur de l'éditeur)
- Convertir le plateau courant en `PuzzleData` v2 (zones, ordre des decks, cartes en
  jeu avec états, méchant, complot, rencontre).
- Test d'aller-retour : état → puzzle → rechargement → état identique.
- **FAIT (23/10)** : `src/game/puzzle/puzzle_capture.py` (`CapturePuzzle(world)` rend le
  `PuzzleData` v2 + une liste `avertissements` de tout ce qui n'a pas pu être capturé).
  Piles dans les champs du format (dessus en premier) ; le reste en commandes
  `Puzzle.RestoreState(cible, key=…)` (identité, méchant, complot principal) et
  `Puzzle.RestoreCard(clé, id, kind, siege=…, host=…)` (alliés, soutiens, sbires engagés,
  complots annexes, environnement, améliorations). Chaque carte posée porte une **clé** :
  viser par identifiant serait ambigu avec un double dans un deck. Les compteurs, jetons et
  cartes d'état sont des valeurs **absolues** (une carte arrive en jeu avec ses compteurs de
  départ). Stades du méchant / du complot : position dans les listes de la campagne (un
  `AdvanceMainScheme` = un stade). 3 cas d'aller-retour dans `outils/test_puzzle_moteur.py`
  (`capture_*`), la capture rechargée dans un processus neuf est identique.
- **Pas encore capturé** (signalé en avertissement : réserve, rising tide, cartes distribuées, deck annexe, ressources, face cachée ; ignoré : le reste) : cartes glissées sous une
  autre, obligations en jeu, ressources en réserve, deck annexe (écureuils, invocations),
  cartes retournées / face cachée, contrôleur d'un sbire non engagé, cartes spéciales
  d'un mode (ville Punisher).

### E5. Création : assistant guidé, puis plateau libre
**Avancement E5 (23/10)** : couche de données faite, interface pas commencée. Le brouillon de
l'assistant et sa traduction en puzzle v2 vivent dans `public/js/prepare/puzzle-brouillon.js`
(module pur, tourne sous Node ; mêmes commandes `Restore*` que la capture). Cas
`brouillon_vers_moteur` : le puzzle produit en JS est monté par le moteur et sa capture redit
la même chose. Décision (23/10, laissée à Claude) : le créateur s'ouvre depuis le panneau
« Puzzles » (`puzzles.js`, bouton « Créer un puzzle »), en modale orange plein écran ; ce panneau
est débranché du site à la demande de l'utilisateur, il se rallume à la livraison.
**E5 assistant FAIT (23/10)** : `public/js/prepare/puzzle-assistant.js`, 8 étapes (les mains et les
decks sont réunis en une étape « Les cartes des héros »), modale orange, Retour / Passer / Suivant,
Tester (envoie le puzzle à `/new_puzzle`, ouvre le plateau), brouillon enregistré à chaque étape
dans le navigateur avec proposition de reprise. Test navigateur rejouable :
`node outils/test_puzzle_assistant.mjs [dossier_captures]` (le jeu doit tourner, `LANCEUR-LINUX.sh`).
Limites connues : le panneau Objectifs n'apparaît qu'avec le plateau COMPILÉ (recopie au
déploiement) ; pas encore de glisser-déposer (ordre par flèches) ; pas de ressources en réserve ;
pas d'avertissements doux (deck illégal) ; pas de « Affiner sur le plateau » ; pas d'aperçu en
direct ; l'édition de l'ordre du deck de rencontre n'est pas proposée (ordre du scénario).
Principe (décision du 22/10) : **hyper simple et intuitif**. Un assistant à ordre
fixe, une étape par écran, barre de progression, bouton Retour, bouton Passer :
toute étape est facultative et se règle avec des valeurs par défaut raisonnables.
Chaque étape montre un aperçu en direct de la situation.

Étapes (ordre logique, du général au détail) :
1. **Qui joue** : nombre de héros, héros, deck de chacun (decks de départ proposés).
2. **L'ennemi** : méchant, stade, mode expert/standard, sets de rencontre.
3. **L'état de la menace** : PV du méchant, complot principal (étape, menace).
4. **Les mains** : cartes en main de chaque héros (recherche + glisser).
5. **Les decks** : ordre des decks héros et rencontre (liste glissable, mélanger).
6. **Ce qui est en jeu** : alliés, soutiens, améliorations, serviteurs, complots
   annexes, attachements (ajout par recherche, glisser sur le plateau).
7. **Les états** : PV des héros, dégâts, statuts, compteurs, prêt/épuisé, ressources,
   premier joueur, phase de départ. Clic sur une carte = petit panneau à gros boutons.
8. **L'objectif** : cases à cocher (vaincre, survivre, terminer le complot…), texte
   libre, indices.
9. **Présentation et test** : titre, histoire, difficulté ; bouton Tester ; solution
   de référence facultative ; Publier.

Règles de conception :
- Un seul geste par action (clic ou glisser), jamais de menu caché obligatoire.
- Texte clair en français, bulles d'aide, aucun jargon de moteur.
- Contrôle en direct : avertissement doux si deck illégal ou situation incohérente
  (ex. héros à 0 PV), jamais bloquant.
- **« Affiner sur le plateau »** à tout moment : bascule sur le vrai plateau en mode
  édition (catalogue, clic droit, jetons, annuler/refaire Ctrl+Z/Y, bouton
  Tester/Éditer). On peut revenir à l'assistant ; les deux modifient le même état.
- Brouillon sauvegardé automatiquement dans le navigateur à chaque étape.
- Chaque étape = un composant indépendant, testable seul (Playwright).
- Tests d'utilisabilité : faire créer un puzzle à quelqu'un qui n'a pas vu l'outil ;
  le premier puzzle doit prendre moins de 5 minutes.

### E6. Publication (côté client)
- Écran titre/description/difficulté/indices/objectifs/visibilité de la solution.
- Enregistrement optionnel de la solution de référence (replay) ; mention
  « non vérifié » sinon.
- Affichage du code, du lien et de la clé d'édition (une fois, puis dans Mes puzzles).

### E7. Serveur de puzzles
- API : publier, lire par code, modifier/supprimer avec la clé, stockage disque.
- Codes courts uniques (type PZ-A4F9), liens cliquables, limites de taille et de
  débit, validation stricte du contenu (liste blanche des commandes).
- Aucune donnée personnelle : pseudo libre uniquement.
- **Conservation : 28 jours** à partir de la dernière fois où le puzzle a été joué
  (la création compte comme premier jeu). Chaque partie lancée par quelqu'un remet le
  compteur à zéro. Passé 28 jours sans jeu, le puzzle est supprimé automatiquement
  (nettoyage périodique côté serveur). Le créateur peut aussi le supprimer avec sa clé.
- Prévoir l'affichage « expire dans N jours » dans Mes puzzles, et l'avertissement
  au créateur d'un puzzle proche de l'expiration (côté navigateur, à l'ouverture).

**E7 FAIT (23/10)** : `site/puzzles_publies.py` (stockage SQLite, codes `PZ-XXXX`, clé d'édition dont seule
l'empreinte est gardée, liste blanche de commandes de mise en place — ni `Win`, `Lose`, `End` ni
`ValidateObjective` —, validation stricte du moteur à la publication ET à la lecture, cartes inconnues
refusées, 28 jours depuis le dernier jeu, nettoyage paresseux), `site/api_puzzles.py` (routes
`GET /api/puzzle/PZ-XXXX[?jouer=1]`, `POST /api/puzzle/publier`, `.../modifier`, `.../supprimer` ;
CORS limité au domaine, ses sous-domaines et le jeu local ; freins par adresse : 10 publications par
heure) branchées dans `orchestrateur.py` (`do_GET`, `do_POST`, `do_OPTIONS`). Tests :
`python3 site/test_puzzles_publies.py` (53), `python3 site/test_api_puzzles.py` (serveur HTTP réel),
`python3 outils/test_puzzle_format.py` (garde-fou : défauts et commandes permises vs moteur).
**Pas déployé** : la route `/api/puzzle/` n'existe sur le site qu'après déploiement ; Caddy n'a rien
à changer (même service que le site). Restent : « Mes puzzles » (E9), l'envoi depuis l'assistant (E6).

### E8. Résolution
- Écran d'intro (titre, histoire, difficulté, objectif) puis plateau.
- Bandeau d'objectif repliable ; indices un par un ; annuler et recommencer
  illimités ; decks cachés mais ordre fixe (même graine à chaque essai).
- Solution de référence : visible ou non selon le choix du créateur.
- Résolution sur mobile/tablette (l'édition reste PC).

**E8 FAIT en grande partie (23/10)** : l'énoncé (titre, histoire, difficulté, indices, auteur) voyage
du puzzle à l'écran : `Scene.puzzle_info` → `WorldDescriptor.puzzle_info` → `ui-app/src/board/PanneauEnonce.tsx`
(introduction plein écran une seule fois par puzzle, panneau repliable en haut à droite, indices dévoilés
un par un, « Relire l'introduction », « Recommencer » en deux temps qui renvoie le puzzle courant gardé
par `puzzle-client.js` à `POST /new_puzzle`). Mémoire dans `sessionStorage`, par puzzle. 6 tests vitest,
2 cas moteur (`enonce_*`). « Annuler » existait déjà sur le plateau. **Pas fait** : solution de référence
(enregistrer / rejouer un replay, visibilité `after/always/never`), plateau mobile, test dans le vrai
plateau (le plateau compilé ne se recopie qu'au déploiement, `ui-app/deployer.sh`, non lancé).
Batterie complète à lancer en fin de chantier (`scene.py` touché).

### E9. Accueil et « Mes puzzles »
- Le bouton Puzzle ouvre un menu à 3 choix : Résoudre par code, Créer, Mes puzzles.
- Mes puzzles : créés (brouillons + publiés, code, clé), résolus, en cours,
  sauvegardés par code (stockage navigateur).
- Remplacer `puzzles.js` et l'ancien `puzzle_editor.html`. **Les 7 puzzles
  existants sont supprimés** (décision du 22/10) : fichiers `puzzle/*.json`, routes
  et copie dans le paquet navigateur (`construire.py`) à retirer proprement.

### E10. Hors ligne et navigateur
- Création/résolution locales dans la version navigateur (Pyodide) ; publication et
  lecture par code seulement avec le serveur.
- Contrôle d'équivalence moteur serveur / navigateur sur les nouveaux scénarios.

**E10 FAIT (23/10)** : le paquet navigateur se reconstruit depuis les sources (`python3 navigateur/construire.py
--sans-pages`, `dist/` ignoré par git) et embarque donc `puzzle_capture.py`, `RestoreCard/RestoreState`, la validation
et `POST /new_puzzle` (le shim `navigateur/src/shim.js` transmet déjà le corps des POST). Contrôle d'équivalence
des puzzles : `python3 navigateur/essais/equivalence_puzzle.py` (moteur normal Python 3.10 contre Pyodide 3.12 sur
3 puzzles : la CAPTURE de l'état monté doit être identique) → 3 identiques. La création et la résolution hors
ligne marchent ; publier et lire par code demandent le site (`urlSite()` rend null hors ligne, message clair).
Pas encore essayé : l'assistant et le plateau eux-mêmes dans le navigateur (`navigateur.html`).

### E11. Robustesse
- Garde de compatibilité : après modification d'une carte, rejouer les solutions de
  référence et marquer les obsolètes.
- Tests UI (Playwright, dossier `ui-check`) : créer, tester, publier, résoudre,
  modifier, supprimer, reprise après rechargement, mobile en résolution.
- Batterie complète en fin de chantier (gros regroupement), filtres ciblés entre
  les étapes.

### E12. Documentation et fin
- `docs/puzzle/` : guide créateur et guide technique ; mise à jour de `docs/README.md`.
- Commit par étape. **Pas de déploiement sans demande** ; avant tout déploiement,
  vérifier les joueurs en ligne. Push GitHub seulement en fin de session.

## Ordre et dépendances
E0 → E1 → E2 → E3 → E4 → E5 → E6 → E7 → E8 → E9 → E10 → E11 → E12.
E7 peut avancer en parallèle de E5/E6 dès que E1 est figé. E4 est le point à plus
haut risque : à attaquer tôt et à valider par l'aller-retour avant l'interface.

## Risques
- Capture d'état exhaustive (cartes avec effets en cours, attachements, jetons
  rares, modes particuliers comme la ville Punisher).
- Déterminisme : le même ordre de decks et la même graine à chaque essai, y
  compris dans le navigateur.
- Scripts de cartes qui changent : puzzles et solutions à revalider.
- Taille de l'assistant et du plateau libre : l'interface est la plus grosse part du travail ; la simplicité demande plusieurs essais de maquette.

## Décisions du 22/10
- Les 7 puzzles existants sont supprimés.
- Création par assistant guidé à ordre fixe, étapes facultatives, plateau libre en option.
- Puzzles publiés conservés 28 jours depuis le dernier jeu ; tout jeu remet le compteur
  à zéro.

## Avancement
- **E0/E1 faits** (22/10) : `puzzle_data.py` v2 (compatible v1), `puzzle_validation.py`,
  `outils/test_puzzle_format.py` (12 fichiers v1 relus, 30+ commandes hostiles refusées).
- Constat : `PuzzleHelper.Exec` laisse passer les commandes sans appel (voir
  FORMAT-V2.md) → corrigé en E3 (v2) et filtré à la publication/lecture en E7.
- Interface : les modales et panneaux d'édition sont **en orange** (consigne du 22/10).
- Prochaine étape : E2 (moteur, mise en place complète, 1 à 4 héros).
