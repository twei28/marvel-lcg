# Hellfire Hunt, scénario 1 « White Queen » (Dipsome), préfixe `hf` : gabarits PROCESSUS-CARTE

Worktree `Marvel-LCG-campagnes`, branche `campagnes-fanmade`. Pack `hellfire_hunt_white_queen` (set 240), module plat `src/cards/pack/hellfire_hunt_white_queen/`.
Scénarios : `hellfire_white_queen` (standard : stades A1/B1 puis A2/B2) et `hellfire_white_queen_expert` (A2/B2 puis A3/B3). Cas : `tools/cas/hellfire_white_queen.py` (noms `[hf] ...`).
Génération des données (idempotente) : `docs/packs/hellfire-hunt-white-queen/generer_donnees.py` (copie de travail du 26/10/2026).

## ÉTAT NET (26/10/2026, PAUSE demandée par l'utilisateur)

Vérifié à l'instant : `python -m compileall -q src` passe, JSON valides (cards, sets_info, 2 scénarios). Rien n'est commité, rien n'est à moitié écrit.

### Extensions moteur
- **« Forme de vilain sans remise à zéro des PV » : FAITE, aucun code moteur nécessaire.** `villain.card.Flip(effect)` garde dégâts/statuts/attachements ; `scenario.AdvanceVillainStage` révèle le stade suivant dans la même forme (face partageant le plus de traits). Preuves : cas `hf101a/hf101b ...`.
- Seul ajout moteur : trait `DIAMOND` dans `src/game/card/face/card_face.py` (liste TRAITS).
- **« Incite 1 » au retour en PSIONIC** : codé dans le script de hf103a (`AfterCardFlipToThisSide` + `MenaceSurLeComplotPrincipal`) car la clé `Incite` dans la desc d'un vilain plante (`KeyError: 'Incite'`). À faire éventuellement : support natif de la clé sur un vilain.
- Hors scénario (autre agent) : decks de table Recruited Mutants / Potential Ally, PV persistants (expert).

### Cartes (42) : 94 cas `[hf]` TOUS VERTS (dernière passe PARALLELES=6, filet anti-Traceback actif)
- **Terminées côté code et prouvées par cas** : hf101a/b, hf102a/b, hf103a/b, hf104a/b, hf105a/b, hf106a/b, hf107, hf110, hf111, hf112, hf114–118, hf120, hf122, hf124, hf125 ; Perfection hf301–308 ; Conclave hf311, 312, 313, 317, 318 ; Delusion hf321, 322, 324, 325.
- Statut officiel : « Carte terminée : NON (provisoire) » pour toutes tant que : preuve par substitution non faite, test humain non fait.
- Approximations/doutes à poser à l'utilisateur (QUESTIONS.md PAS ENCORE ÉCRIT) : 1B « avance après la fin du round » + report du jeton d'accélération ; hf304 « attaques contre vous » en multijoueur ; Incite du stade 3 à la première révélation.

### PAS COMMENCÉ
- Preuve par substitution (`tools/substituer_pack.py <game_dir> <port> hf`, ⚠ sauvegarder le pack avant : non commité).
- Textes français des 42 cartes (`ui-app/src/board/textes-fr-fanmade.ts` + `node ui-app/outils/generer-traduction-public.mjs`), contrôle de voile des scans.
- Autoplay (8 parties Sunspot `sunspot_hellfire` + un témoin sur `hellfire_white_queen`), vérificateur de decks, `test_newgame`.
- QUESTIONS.md, recette RECETTES-MOTEUR, gabarits PROCESSUS-CARTE détaillés par carte.

### Pour reprendre
- Worktree `/home/oem/Desktop/Marvel-LCG-campagnes`, branche `campagnes-fanmade`. Ne JAMAIS toucher `/home/oem/Desktop/Marvel LCG`. Venv `.venv-linux`.
- Fichiers : `Fusion/marvel-lcg-src/data/{cards.json (pack hellfire_hunt_white_queen), sets_info.json (clé 240), encounter_sets/hf_*.json, scenarios/hellfire_white_queen[_expert].json}`, `src/cards/pack/hellfire_hunt_white_queen/__init__.py` (helpers) + scripts hfNNN, `tools/cas/hellfire_white_queen.py`, `assets/pics/hf*.jpg`, générateur `generer_donnees.py` (idempotent).
- Test (depuis `Fusion/marvel-lcg-src`) : `PARALLELES=6 CAS_PREFIX=hfw ../../.venv-linux/bin/python tools/test_capacites.py "$PWD/.game-src-hfw" 9800 <sortie.json> "[hf]"` (ports 9800–9899, game_dir `.game-src-hfw`).
- Numéros réservés : hf001–hf099 fondations (autre agent), hf100–hf199 scénarios, hf300–hf399 modules.

### Pièges de harnais appris (à recopier dans RECETTES-MOTEUR)
- `Puzzle.CreateEncounterDeck(a, b, c)` pose `a` en DERNIER : la dernière carte créée est le DESSUS du deck.
- `Puzzle.EmptyHand()` en tête de mise en place + `main_exclusive` : sinon le pilote joue « Great Responsibility » en remplacement d'une pose de menace.
- `Puzzle.BeginVillainPhase()` ne fait pas activer le vilain : `Puzzle.Attack('<vilain>')` / `Puzzle.Scheme('<vilain>')`.
- Payer deux ressources de types différents (`BR`) : `payer_avec=[genius, strength]` + `payer_tout=True`.
- Un « MayChooseOneAbility » : le pilote l'ACCEPTE par défaut ; `choisir_option="Cancel"` pour refuser.
- Un `game_dir` à soi (`.game-src-hfw`) : un autre harnais peut tourner sur `.game-src-par*`.
- Hero en forme HEROS : le pilote DEFEND ; pour mesurer des dégâts, `Puzzle.Exhaust('01001a')` ou rester en alter-ego (Quickstrike ne s'applique qu'à un HEROS).
