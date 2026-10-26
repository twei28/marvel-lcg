# Hellfire Hunt (Dipsome) : fondations de campagne, cartes de campagne et d'aspect (préfixe `hf`, hf001-hf099)

Branche `campagnes-fanmade`, worktree `/home/oem/Desktop/Marvel-LCG-campagnes`. Pack `hellfire_hunt` (set 234), un module par carte (`src/cards/pack/hellfire_hunt/hfNNN.py`).
Cas : `tools/cas/hellfire_hunt.py` (préfixe de nom `[hfc]`), lancés par `PARALLELES=6 CAS_PREFIX=hfa python tools/test_capacites.py <game_dir> 9710 <rapport> "[hfc]"`.
Importeurs : `tools/importer_cartes_hellfire_hunt.py` (cartes -> `data/cards.json`) et `tools/importer_images_hellfire_hunt.py` (images -> `assets/pics/hf*.jpg`).
Aucune carte n'est « terminée : OUI » : aucune partie réelle jouée par un humain.

## ÉTAT NET (26/10/2026, relevé en fin de passe n°1)

### Prouvé par un cas test_capacites (vert) : 92 cas sur 92 (dernier run complet `[hfc]`)

| Bloc | Cartes | État |
|---|---|---|
| Alliés RECRUITED (200-214) | hf013 Armor, hf014 Blink, hf015 Dazzler, hf016 ForgetMeNot, hf017 Marrow, hf018 Glob Herman, hf019 Mirage, hf020 Oya, hf021 Polaris, hf022 Sage, hf023 Wiz-Kid, hf024 Wolfsbane, hf025 Emma Frost, hf026 Charles Xavier, hf027 Sebastian Shaw, hf028 Selene | 16/16 scriptés, 1 à 3 cas chacun, tous verts |
| Manigances POTENTIAL ALLY (188-199) | hf029 à hf040 | 12/12 scriptées, cas « défaite -> l'allié sort de côté » pour chacune + cas propres (hf030 hasard, hf033, hf034, hf036, hf037, hf038, hf040), tous verts |
| Manigances de campagne (180-186) | hf041 Cerebro Insights, hf042, hf043, hf044, hf045 Rally the Survivors, hf046, hf047 | hf042-hf047 verts ; hf041 CORRIGÉ : `AbilitePotentialAlly` n'exige plus `has_defeating_player=True` (défaite par effet sans joueur vainqueur), cas vert |
| Environnement (187) | hf048 Xavier's Institute | Action (pioche du deck Recruited) et Réponse forcée (défausse Recruited) verts ; permission de jouer Blink depuis la défausse Recruited verte |
| Cartes d'aspect de Marvel Girl | hf001 Boom Boom, hf002 Captain Britain (Brian), hf003 PAC-RAT II, hf004 Divided We Fall, hf005 First Command, hf006 White Phoenix, hf007 Jump-Start, hf008 Psionic Soulmates, hf009 From The Ashes | 9/9 scriptées, cas verts |
| Reskins | hf010 Energy, hf011 Genius, hf012 Strength | données + images + collection `sunspot_hellfire` / `rachel_summers` (variantes.ts, app.js, test) |
| Module de campagne | `src/cards/pack/hellfire_hunt/campaign.py` | mise en place commune (16 alliés de côté, deck Recruited, 1 POTENTIAL ALLY par joueur, étapes des scénarios 1, 3, 5), relevé du carnet : 8 cas verts |
| Carnet | `data/campagnes/hellfire_hunt.json` | clés vérifiées par `tools/verifier_campagnes.py` (OK) |
| Moteur (E2, E3) | deck Recruited Mutants de table (`RecruitedMutants`, `AjouterAuxRecrutes`, `PiocherDesRecrutes`), `Puzzle.PutIntoRecruitedMutants`, `PlayFromRecruitedDiscard`, `HellfireCampagne`, `HellfireReleve` | verts |
| Textes français | `textes-fr-fanmade.ts` (48 textes, hf001-hf048), copie publique régénérée | tests de vocabulaire verts ; voiles des 48 scans : PAS vérifiés |

### Fait après le relevé ci-dessus (PAUSE de la campagne demandée par l'utilisateur, 26/10/2026)
- Decks de départ remplis ET montés (`DECK_NOM=… tools/verifier_tous_les_decks.py`, ports 9721/9722, OK) :
  - `rachel_summers.json` : 22 cartes (livret p.20 ; X-Gene en 1 seul exemplaire, « Max 1 per player » : à trancher) ;
  - `sunspot_hellfire.json` : 15 cartes SEULEMENT (Cable 45011, Domino 41031, Forge 36022, Warpath 42013, Battle Fury 06018/35015, Combat Training ×2, Caliban 40014, Adrenaline Rush ×3, Energy/Genius/Strength). Choix des versions de Cable/Domino/Warpath non vérifiés (aspect). ABSENTES du zip et du jeu : Finishing Blow ×3, Cecilia Reyes, For What's Right ×3, X-Force Strike ×3 ; nemesis « Mutant Kidnapping » non rapproché.
- Perte de campagne au scénario 5 en expert (E9) : déclarée en données dans `data/campagnes/hellfire_hunt.json` (`defaite: partie_perdue, expert_seulement`), lue par `ui-app/src/board/campagne/defaite-campagne.ts`. Pas de test vitest ajouté, pas testée en jeu. `tools/verifier_campagnes.py` OK.
- `python -m compileall -q src` OK, JSON valides.

### RESTE (rien de ceci n'est fait)
- Preuves par substitution (module retiré -> cas rouge -> restauré) pour chaque carte ;
- cas manquants : Rally the Survivors (buff en pile de victoire), limite once-per-phase de hf048, hf043 (Action de Xavier bloquée), flip White Queen de hf041 (cartes du scénario 1 d'une autre fork), hf004 / hf005 (témoins), jeton d'accélération en expert (code présent dans `_campagne_experte`, non prouvé par un cas), E9 ;
- `docs/packs/hellfire-hunt/QUESTIONS.md` NON écrit. Doutes : X-Gene ×2 vs Max 1 ; texte de hf044 Psychic Minefield ; Rally the Survivors « reste en jeu » ; permission de jouer Blink portée par hf048/hf045 ; cartes absentes de Sunspot ; Aggression officielle vs fan-made ; unicité Emma/Captain Britain ;
- `tools/recalculer_checksums.py`, `test_cards`, `verifier_prefixes` (préfixe `hf` partagé avec la fork White Queen), `verifier_appels_modules`, `verifier_api_cartes`, `generer_arts_cartes.py --verifier`, autoplay des decks : non relancés après les derniers correctifs ;
- scénarios 1 à 5 : hors périmètre (autre fork, hf100-hf199 et hf300-hf399) ;
- voiles FR des 48 scans non vérifiés ; `RECETTES-MOTEUR.md` (E2/E3) non mis à jour.

### Pour reprendre
- Interpréteur : `/home/oem/Desktop/Marvel-LCG-campagnes/.venv-linux/bin/python`, depuis `Fusion/marvel-lcg-src`, game_dir `$PWD/.game-src`, ports 9700-9799 (9701 test_cards, 9710 test_capacites, 9721-9722 decks).
- Cas : `PARALLELES=6 CAS_PREFIX=hfa python tools/test_capacites.py "$PWD/.game-src" 9710 <rapport.json> "[hfc]"`.
- Lire : `tools/cas/hellfire_hunt.py`, `src/cards/pack/hellfire_hunt/{__init__,campaign}.py`, `tools/importer_cartes_hellfire_hunt.py`, `docs/rapports/2026-10-26-hellfire-hunt-lecture-livret.md`.
- Numéros réservés : hf001-hf099 (moi, utilisés jusqu'à hf048) ; hf100-hf199 et hf300-hf399 = autre fork. `data/cards.json` seulement par script sous `flock /tmp/cards_json.lock`.
- Rien n'est commité ; `deployer.sh` non lancé.
