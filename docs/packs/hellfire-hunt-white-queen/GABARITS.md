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

## Finitions du 01/11/2026 (session « finitions Hellfire Hunt »)

- Outil de preuve sur COPIE PRIVEE (jamais sur les sources partagees) : `docs/packs/hellfire-hunt/substituer_prive.py <pack> <port> <sortie.json>` (generalisation de celui de Torn ; `HFF_TAG='[hfc]'` pour les fondations). Mutations ponctuelles : un seul fragment du module retire, le cas doit tomber au rouge.
- **Modules sans cas** (rouges 0/0 au rejeu prive) : `hf102a` (Reponse forcee forme A du stade 2), `hf103b` (Interruption forcee forme B du stade 3 expert) : AUCUN cas ne les visait (module vide, 22 cas verts). Cas ajoutes : `hf102a Reponse forcee`, `hf103b Interruption forcee` + temoin ; rouges si le module est vide (preuve par substitution refaite). `hf105a` et `hf106a` sont couverts par les cas `hf104b` / `hf105b` (rouges quand on les vide). `hf103b` porte aussi la Reponse forcee B couverte par `hf103a Incite 1`.
- **hf308 Illusion Loop, branche Boost** : le cas existant n'avait AUCUNE attente (`{}`, vert quoi qu'il arrive). Refait : un attachement ILLUSION sur l'identite -> Confused (rouge si la branche Boost est retiree) + temoin sans attachement. Balayage de TOUS les fichiers `tools/cas/hellfire_*.py` : plus aucun cas a attendu vide.
- Verts sans module (rejeu prive) : stades vaincus en meme forme (logique du moteur), `hf106b` « If this stage is completed, the players lose the game » (lu NATIVEMENT dans le texte, scheme_main.py), valeurs imprimees (`desc`), temoins (hf101b, hf103a, hf107, hf301, hf124/125...). Aucun cas nominal vert par erreur apres les corrections ci-dessus.

## Correctifs texte/code du 02/11/2026 (hf304 Illusory Defender, hf306 Psionic Projection)

Harnais `hfp` (`.game-src-hfp`, ports 11400-11499). Rouge avant correctif vu sur les cas neufs ; substitution (module ou fragment retiré) refaite après, sorties ci-dessous. Texte FR inchangé (aucun écart de texte, seulement de code).

### hf304 : Illusory Defender
- [x] Étape 2 : références : `UnitCannotDefend` (sk201 / 27152), `AfterUnitAttackYou` (55039). Message `CheckIfUnitCanDefendAgainstAttack` : n'avait que le défenseur et l'attaquant.
- [x] Étape 5 : texte-contre-code. Mots-pièges : `against you` (portée), `allies or other identities`, `cannot`. Deux écarts trouvés : (1) la restriction valait pour TOUTE attaque (faux à plusieurs joueurs : un allié aurait été empêché de défendre un AUTRE joueur) ; (2) `CardFinder(Ally | Hero)` interdisait aussi au PORTEUR de défendre avec sa propre identité, alors que le texte n'exclut que les alliés et les AUTRES identités.
      Correctif : ajout additif moteur `attacked_targets` (`Message.CheckIfUnitCanDefendAgainstAttack(unit, attacker, attacked_targets=None)`, `IsCanDefense(attacker, attacked_targets=None)`, et `ability.py` passe `message.attacked_targets` depuis la condition de défense) ; le script ajoute deux conditions : la cible de l'attaque est l'identité du porteur, et le défenseur n'est pas l'identité du porteur. Cible inconnue (appelant qui ne la donne pas) : on restreint, comme avant. Aucun autre script ne change de comportement (paramètre optionnel).
- [x] Étape 6 : nombres : 1 compteur illusion retiré après l'attaque du vilain, 2 compteurs si PSIONIC (inchangés).
- [x] Étape 7 : cas (tous verts, 10 `hf304`) :
      - 2 joueurs, allié de l'autre joueur refusé contre une attaque visant le porteur : `hf304 Illusory Defender, 2 joueurs : l'allie de l'AUTRE joueur ne peut pas defendre...` ; l'autre héros refusé aussi.
      - 2 joueurs, attaque visant l'AUTRE joueur : défendable par son allié, par l'allié du porteur, par le porteur : ROUGE avec l'ancien code, vert après.
      - Le porteur défend contre l'attaque qui le vise : ROUGE avec l'ancien code, vert après.
      - Parcours réel de la capacité DEF de l'allié (condition posée par `ability.py`, message d'attaque réel, 2 joueurs) : rouge avec l'ancien code ET rouge si `ability.py` ne transmet plus la cible (substitution M7).
      Limite de harnais : le pilote de test ne choisit jamais un allié comme défenseur, d'où l'évaluation de la condition de la capacité DEF avec un message d'attaque construit (attendu `defense_reelle`).
- [ ] Étape 8 : autoplay : non refait pour ce correctif (rejeu `[hf` complet, voir rapport). Carte terminée : NON (provisoire) : partie humaine à faire.

### hf306 : Psionic Projection
- [x] Étape 2 : références : gb011 et 50173 (même libellé « additional cost to use a basic power » : `AdditionalCostToAttack` + `AdditionalCostToThwart` + `AdditionalCostToDefense`). Le commentaire de gb011 écarte la récupération parce que le moteur n'a pas de coût additionnel pour elle ; ce n'est pas une décision de règle.
- [x] Étape 5 : texte-contre-code. Mots-pièges : `your hero`, `a basic power`, `basic attack or a basic thwart`. Écarts : (1) le coût n'était pas posé sur la DÉFENSE (Rules Reference 1.8 p.10 : cinq pouvoirs de base, dont DEF ; commentaire « la défense n'est pas un pouvoir » faux) ; (2) la Réponse forcée `AfterUnitUseBasicPower` n'avait pas de filtre `powers` : elle se déclenchait aussi après une DÉFENSE alors que le texte ne vise que « basic attack or a basic thwart ».
      Récupération (REC) et manigance (SCH) : « your HERO » = forme héros, qui n'a QUE ATK, THW et DEF dans le moteur (`factory.py` : `REC` n'existe que sur l'alter-ego, SCH n'est pas un pouvoir de héros) : aucun point d'extension moteur nécessaire, rien à ajouter. Si une lecture voulait « identité » (alter-ego inclus), le texte dirait « your identity ».
- [x] Étape 6 : nombres : 1 ressource [mental] (`Cost("B")`, lue contre rm004), 1 compteur retiré par attaque/contre, 2 compteurs si PSIONIC (inchangés).
- [x] Étape 7 : 5 cas verts : attaque (coût + compteur), contre (coût + compteur ; test de l'existant), DÉFENSE (coût) ROUGE avant correctif / vert après, Réponse forcée muette après une défense (compteur reste à 2) ROUGE avant / vert après, témoin sans carte (défense gratuite, héros incliné donc il défend bien).
      Piège de harnais : `Puzzle.Attack(..., defender=)` court-circuite la capacité DEF et son coût (il ne mesure donc PAS le coût) ; le pilote défend de lui-même avec le héros si on n'écrit pas `defender=`.
- [x] Substitutions (module ou fragment retiré, cas rouge, puis remis, vert) : sans `AdditionalCostToDefense` -> rouge (cas défense) ; sans `powers=["ATK","THW"]` -> rouge (cas Réponse forcée) ; sans `AdditionalCostToThwart` -> rouge (cas contre) ; module hf306 vide -> 4 rouges sur 5 (le témoin reste vert) ; module hf304 vide -> 7 rouges sur 10 (3 témoins/cas d'absence verts) ; ancien hf304 -> 3 rouges ; `ability.py` sans la cible -> 1 rouge.
- Rejeu `[hf` complet (harnais hfp, PARALLELES=6) : 717/718, seul rouge hf503a (instabilité connue sous charge, 2/2 verts isolé), 0 Traceback ; test_cards ok=8103 err=0 ; compileall 0.
- Carte terminée : NON (provisoire) : test humain non fait.
