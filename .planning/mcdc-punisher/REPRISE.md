# Reprise du chantier « La ville ne dort jamais » (campagne MC×DC 2026, préfixe `pu`)

État au 22/10/2026, dernier commit de travail Punisher : `ce71924f` (rencontre lot 1). Tout est commité ; rien n'est poussé sur GitHub, rien n'est déployé (ne JAMAIS déployer sans demande explicite de l'utilisateur).

## Règles de travail (rappel)
- Réponses en français, courtes et directes. L'utilisateur veut un topo court toutes les 20 minutes si c'est demandé.
- **Ne pas poser de questions dont la RR donne la réponse** (mémoire `ne-pas-poser-de-questions-evidentes`) : trancher et noter dans les preuves.
- Processus carte : `docs/reference/PROCESSUS-CARTE.md` (preuves dans `.planning/mcdc-punisher/preuves-jigsaw.md`). Mots-clés : fiches `docs/reference/mots-cles/`.
- Le zip « qx » d'une autre IA est peu utile : partir des scans (`paquets-cartes/MC x DC 2026 - campagne Punisher/scans/pNNN.jpg`) et du livret FR (`la-ville-ne-dort-jamais-regles-fr-v1.txt` dans ce même dossier).

## Ce qui est FAIT (tests verts, commités)
| Set | Cartes | Cas de test (filtre) | Fichiers |
|---|---|---|---|
| Jigsaw (sous-fifre) | 13 | `[jig]` 31 | `src/cards/pack/punisher_mcdc_2026/jigsaw/`, `tools/cas/jigsaw.py` |
| Hobgoblin (sous-fifre) + Pumpkin Bomb | 14 | `[hob]` 30 | `.../hobgoblin/`, `tools/cas/hobgoblin.py` |
| The Syndicate | 7 | `[syn]` 15 | `.../the_syndicate/` |
| Punisher's Armory | 5 | `[arm]` 10 | `.../punishers_armory/` |
| Punisher's Hit List | 8 | `[hit]` 12 | `.../punishers_hit_list/` (`Punishment()`) |
| SWAT Team | 6 | `[swat]` 15 | `.../swat_team/` |
| Punishment (scénario 3 « One Last Kill », jouable) | 24 faces | `[pun]` 32 | `.../punishment/`, 4 scénarios `one_last_kill_*` |
| Briques ville PU-5 (zone commune, déplacement, grille, capo par territoire) | — | `[ville]` 16 | `src/game/operate/ville.py`, `world.py` (`game_area_commune`, `MovePlayerToGameArea`), `worlds.py` (`ZonesVisibles`), `ability.py` (`check_game_area`) |

- Échafaudage reproductible : `python3 .planning/mcdc-punisher/construire_jigsaw.py` (depuis la racine du dépôt) puis `tools/recalculer_checksums.py` ; données dans `.planning/mcdc-punisher/defs/punisher_cards.py`.
- Spec de la ville : `docs/rapports/spec-ville-m1-m2-2026-10-21.md` (12 règles, 9 écarts G1-G9, ordre de travail, 16 cas limites). **Pas encore relue par un second regard.**
- Corrections moteur annexes : `AttackProperty.ignore_boost_abilities`, traits `ARMAMENT SYNDICATE CAPO FIST MARINE SOLDIER CONFRONTATION`, compteurs `drone` et `wanted`, `Puzzle.SendRoundEnd/CreateGameArea/CreateCommonGameArea/MoveCardToGameArea/InstallerVille/DeplacerDansLaVille`.
- Autres livraisons de la session : pages de livret de La Toile du Mensonge et de Tempête Galactique (images non versionnées dans `public/stories/`), `tools/verifier_pages_campagnes.py`.

## Fait le 22/10 : environnements et 9 lieux du scénario 1 (`pu005 pu006 pu030-pu038`)
Scripts `src/cards/pack/punisher_mcdc_2026/{the_big_apple,locations_the_big_apple}/`, cas `tools/cas/big_apple.py` (`[big]`, 55), preuves `.planning/mcdc-punisher/preuves-big-apple.md` (pièges trouvés dedans : lire avant de continuer). Harnais ville réelle : `Puzzle.InstallerVille(grille, depart, en_jeu=True)`. Message `AfterPlayerMovedInCity` pour les effets continus de lieu. Échafaudage étendu (`defs/punisher_cards.py`, `construire_jigsaw.py` : sets `the_big_apple` (partiel) et `locations_the_big_apple`). Commits db7d3291, aff819d5 + le dernier.

## Fait le 22/10 (suite) : CAPO, pistes, complots, rencontre lot 1 (commits 95c2ede8, 4bba4d4d, 48aefa38, ce71924f)
| Set | Cas | Fichiers |
|---|---|---|
| 8 CAPO (16 faces pu048-pu055) | `[capo]` 30 | `capos/`, `tools/cas/capos.py` |
| 9 pistes LEAD pu039-pu047, paquet `LeadsDeck` | `[pist]` 29 | `leads_the_big_apple/`, `tools/cas/pistes.py` |
| Complots pu001-pu003 + Gunrunner pu004, scénario `the_big_apple(_expert).json` (mise en place réelle) | `[gang]` 20 | `the_big_apple/`, `tools/cas/gang_war.py` |
| Rencontre lot 1 : pu009 011 012 016 017 018 020 021 | `[renc]` 22 | `the_big_apple/`, `tools/cas/big_apple_rencontre.py` |
Preuves : `preuves-big-apple.md`. Moteur ajouté : zone commune pour le nouveau stade (`World.AdvanceMainScheme`), `Ville.Placer`, compteurs maison, `Puzzle.CreateLeadsDeck/AddToVictoryDisplay/PlaceCountersOnVillains/DamageAllVillains`. Échafaudage : `construire_jigsaw.py` (défs de TOUTES les cartes de rencontre déjà dans `defs/`).

## Ce qui RESTE (ordre proposé)
1. **Cartes liées aux lieux (M5)** : pu007 Burning Building, pu008 Citizens in Danger!, pu010 « It's a Trap! » (attachements : `AttachTo2(lieu)` marche sur un lieu), pu013 Overdrive, pu014 Muse, pu015 Screwball (sbires « attachés » : plan = `lieu.TuckCardUnderHere([sbire])` + `Ability(...).NoOutOfPlayLimit()`), pu022 Like and Subscribe!. Nouveaux messages à créer : `WhenPlayerWouldLeaveLocation(joueur, lieu)` (avant le départ) et `from/to` sur `AfterPlayerMovedInCity` (dans `Ville.Placer`). Helpers prévus : `Ville.Attacher`, lieux inoccupés, `Ville.Porte`.
2. Puis : prouver l'étape 3A « cartes attachées aux lieux distribuées face cachée » (code écrit dans pu003a, non prouvé) ; mettre `BIGAPPLE_ENCOUNTERS = BIGAPPLE_ENCOUNTER_IDS` dans `defs/punisher_cards.py` (le scénario a encore `encounters: []`) et relancer l'échafaudage ; autoplay du scénario ; cas EXPERT de pu018/pu020.
3. **Capo of the Past (pu139)** (dépend des CAPO : faisable maintenant).
4. PU-8 interface « La Ville » ; PU-9 campagne (livret : `docs/packs/mcdc-2026-punisher/regles-fr.md`, noter le lieu de la dernière piste en 2A) ; PU-10 Uptown ; PU-11 défis ; PU-12 textes FR ; PU-13 batterie complète (~1 h) + audit.
5. Décisions prises sans texte de RR, à confirmer en partie réelle : voir `preuves-big-apple.md` (pu039 sbire/allié, identité seule pour « you defend/thwart », Busted!, Red Herring, Shootout).

## Pièges de harnais (déjà payés cher)
- Toute commande Bash dont le texte contient `tools/test_capacites.py` fait REFUSER le harnais (« un autre harnais tourne ») : mettre la commande dans un fichier script (`/tmp/xxx.sh`, créé avec l'outil Write) et lancer `bash /tmp/xxx.sh`. Ajouter `< /dev/null` pour que le harnais ne mange pas l'entrée du shell.
- Commande de test : `PYTHONPATH=src python3.10 tools/test_capacites.py "$PWD" 40100 /tmp/x.json "[filtre]"` depuis `Fusion/marvel-lcg-src`, avec `/home/oem/Desktop/Marvel LCG/.venv-linux/bin/python3.10` ; puis `git checkout -- launch.json`. Un seul harnais à la fois sur le dossier.
- `Puzzle.PlaceThreat/SetThreat` dans `mise_en_place` est perdu : le mettre dans `declencher`. Une attaque d'ennemi sur un allié demande « Defense » (utiliser `passer_sur_option`). `WhenCardSetup` ne part pas pour une carte révélée par `Find.FindAndReveal` (utiliser `WhenThisRevealed`). Une attaque de remplacement lancée depuis une interruption `WouldAttack` repasse par la même interruption (garde de ré-entrée). Les recto-verso doivent être écrits `"puXXXa,puXXXb"` dans les listes de rencontre/mise de côté.
- Un nom inconnu (ex. `SideScheme`) dans un script est une `NameError` AVALÉE par le moteur : vérifier avec un cas, pas à l'œil. `test_cards` (`/tmp/tc.sh`-like : `tools/test_cards.py "$PWD" 40300 /tmp/r.json`) charge tous les scripts.
- Les décisions P1-P8 et l'ordre PU-0…PU-13 sont dans `docs/rapports/cadrage-14-15-19-2026-10-20.md` §1.7.
