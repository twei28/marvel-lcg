# Les puzzles : guide technique

Plan et décisions : `PLAN.md`. Cahier des charges : `CAHIER-DES-CHARGES.md`. Format du fichier : `FORMAT-V2.md`.
Guide de l'utilisateur : `GUIDE-CREATEUR.md`.

## Le trajet d'un puzzle
```
assistant (puzzle-assistant.js)            partie en cours (moteur)
   brouillon  ──puzzle-brouillon.js──►  puzzle v2 ◄──CapturePuzzle (puzzle_capture.py)
                                          │
        POST /new_puzzle (corps JSON) ◄───┤──► POST /api/puzzle/publier (site)  ─► code PZ-XXXX
              │                           │         GET  /api/puzzle/PZ-XXXX     ◄─ jouerParCode
   play_puzzle : validate_puzzle(PUBLISHED_METHODS) si format ≥ 2
              │
   BuildPuzzleScene (puzzle_scene.py) ─► Scene ─► partie
   (commandes de mise en place = piles, puis puzzle_command)
```

## Où est quoi
| Sujet | Fichier |
|---|---|
| Format et défauts | `src/game/puzzle/puzzle_data.py` |
| Validation stricte + liste blanche `PUBLISHED_METHODS` (source unique) | `src/game/puzzle/puzzle_validation.py` |
| Commandes `Puzzle.*` (dont `RestoreCard`, `RestoreState`) | `src/game/puzzle/puzzle.py` |
| Données → scène (piles, premier joueur, objectifs, énoncé) | `src/game/puzzle/puzzle_scene.py` |
| Objectifs et fin de puzzle | `src/game/puzzle/puzzle_objectives.py` |
| Capture du plateau → puzzle | `src/game/puzzle/puzzle_capture.py` |
| Routes moteur | `engine/device/web/server/server_new_game.py` (`/new_puzzle` GET et POST), `server_get.py` (`/puzzle_objectif`) |
| Serveur de puzzles (SQLite, codes, clés, 28 jours) | `site/puzzles_publies.py`, routes dans `site/api_puzzles.py`, branchées dans `site/orchestrateur.py` |
| Assistant, client, panneau | `public/js/prepare/puzzle-assistant.js`, `puzzle-brouillon.js`, `puzzle-client.js`, `puzzles.js` |
| Énoncé, objectifs sur le plateau | `ui-app/src/board/PanneauEnonce.tsx`, `PanneauObjectifs.tsx` |
| Version navigateur (Pyodide) | `navigateur/construire.py` (rebuild), `navigateur/essais/equivalence_puzzle.py` |

## Pièges mesurés
- **Cartes visées par CLÉ, jamais par identifiant** : `FindOrCreateFace` fouille les decks d'abord ; un double dans le
  deck ferait viser la mauvaise carte. `RestoreCard('e1', …)` crée une carte neuve et la nomme, `RestoreState` règle une
  carte déjà en jeu (identité, méchant, complot principal).
- **`Deck.GetAll()` va du dessous vers le dessus** ; le format 2 donne les piles du dessus vers le dessous (le format 1,
  l'inverse). `BuildPuzzleCommands` inverse selon `puzzle.format`.
- **Compteurs, jetons, cartes d'état en valeur ABSOLUE** : une carte arrive en jeu avec ses compteurs de départ
  (Web-Shooter : 3).
- **1 `AdvanceMainScheme` = 1 stade** ; le stade se lit dans `campaign.villain / schemes`, pas dans la pile de victoire.
- **`AdvanceVillain` sur le dernier stade termine la partie.**
- **Une adresse ne porte pas un vrai deck** (ligne de requête plafonnée à 8 Ko) : le puzzle voyage dans le corps d'un POST.
- **`e.currentTarget` est nul après un `await`** : mémoriser le bouton avant.
- **`PuzzleHelper.Exec` laisse passer les commandes sans appel** (`import os`) : tout puzzle v2 passe par
  `validate_puzzle` à `play_puzzle`, à la publication ET à la lecture.

## Tests
| Quoi | Commande |
|---|---|
| Moteur (≈ 37 cas : mise en place, objectifs, capture, énoncé) | `~/.marvel-venv/bin/python outils/test_puzzle_moteur.py` |
| Format, validation, dérive des défauts et de la liste blanche | `python3 outils/test_puzzle_format.py` |
| Serveur de puzzles | `python3 site/test_puzzles_publies.py` ; `python3 site/test_api_puzzles.py` (vrai serveur HTTP) |
| Module client | `node outils/test_puzzle_client.mjs` |
| Assistant dans un vrai navigateur (le jeu doit tourner : `LANCEUR-LINUX.sh`) | `node outils/test_puzzle_assistant.mjs [dossier_captures]` |
| Interface | `cd ui-app && npx vitest run` |
| Équivalence moteur normal / navigateur | `python3 navigateur/construire.py --sans-pages` puis `python3 navigateur/essais/equivalence_puzzle.py` |
| Batterie complète (≈ 1 h 30, jamais en modifiant `src/`) | `bash Fusion/marvel-lcg-src/tools/batterie_complete.sh --fond` |

## Déploiement
Rien n'est déployé. Le plateau compilé (`public/app`, ignoré par git) ne se met à jour que par `ui-app/deployer.sh`, qui n'est
lancé que sur demande explicite ; avant tout déploiement, vérifier les joueurs en ligne. Les routes `/api/puzzle/` n'existent
sur le site qu'après le déploiement de `site/`.
