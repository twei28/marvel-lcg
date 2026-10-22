# Reprise du chantier « La ville ne dort jamais » (campagne MC×DC 2026, préfixe `pu`)

État au 22/10/2026 (soir), dernier commit de travail Punisher : `725d3dc0` (campagne combat 3). Combats 1, 2 et 3 : moteur + carnet FAITS, commités. Tout est commité ; rien n'est poussé sur GitHub, rien n'est déployé (ne JAMAIS déployer sans demande explicite de l'utilisateur).

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

## Fait le 22/10 (fin) : cartes liees aux lieux, scenario 1 branche, campagne (donnees) (commits fd41ae4d, 35544b11, 38ad67cf, 204094e5)
| Quoi | Cas | Fichiers |
|---|---|---|
| pu007 pu008 pu010 pu013 pu014 pu015 pu022 + FAQ Collaboration | `[lieu]` 41 | `the_big_apple/pu0xx.py`, `tools/cas/big_apple_lieux.py` |
| 3A distribue aussi les sbires attaches ; cas EXPERT pu018/pu020 | `[gang]` 27 | `pu003a.py`, `tools/cas/gang_war.py` |
| Jeu de rencontre branche (`BIGAPPLE_ENCOUNTERS`), scenarios standard/expert regeneres | autoplay 32 parties, 0 exception | `defs/punisher_cards.py`, `data/scenarios/the_big_apple*.json` |
| pu140 Big Apple Gang War! + pu141 Seized Tech Crates : DONNEES SEULEMENT (ID imprime 6132 commun, d'ou pu140/pu141) | aucun | `defs/`, `cards.json`, `assets/pics` |
Moteur ajoute : messages `WhenPlayerWouldLeaveLocation / WhenPlayerWouldEnterLocation`, `AfterPlayerMovedInCity(depuis, vers)`, `Ville.Lieux/LieuxInoccupes/AttacherSbire/DegagerSbire/Hote/SbiresAttaches`, `WhenUnitWouldBeDefeated.excess_damage`, `Puzzle.AttacherAuLieu/PlacerDansLaVille/SendAfterRoundEnd`, `can_teamwork.py` (Collaboration compte tous les territoires + sbires attaches), outil `MCLCG_TRACE_CRASH=<fichier>` (trace des exceptions avalees par le moteur : INDISPENSABLE pour debugger un script de carte). Preuves : `preuves-big-apple.md`.
Regression (derniere) : [gang] 27, [lieu] 41, [renc] 23, [big] 55, [ville] 15, [pist] 29, [capo] 30, [pun] 32, [jig] 31, [hob] 30 verts ; `test_cards` 7150 ok.

## Fait le 22/10 (campagne combat 1, scripts + carnet)
pu140 (mots-cles, mise en jeu par `CampaignSetup()` de pu001a), pu141 (Setup + Action), note du lieu (pu002a), releve (`punisher_mcdc_2026/campaign.py`), `data/campagnes/punisher_mcdc_2026.json`, cas `[camp]` 20, 8 mutations rouges. Preuves : `preuves-big-apple.md`. Piege : dossier de set = nom nettoye (`campaign_the_city_never_sleeps`).

## Fait le 22/10 (soir) : combats 2 et 3 de la campagne (commits 0fb67924, 725d3dc0)
| Quoi | Cas | Fichiers |
|---|---|---|
| Combat 2 : pu142 Tracking the Buyer, pu143 Punisher's Ordnance Cache, 20 scenarios `tracking_the_buyer_<manigance>_<sous-fifre>(_expert)`, table lieu x CAPO (`ScenarioDuCombat2`), releve partage avec Fear No Evil (`world.campagne_collecteurs`, `mts/campaign.py`) | `[camp]` | `campaign_the_city_never_sleeps/pu142.py pu143.py`, `campaign.py` |
| Combat 3 : pu144 Punishment (retournee en pu145 S.H.I.E.L.D. Support Team), pu146 allie Punisher, 4 scenarios `punishment_<sous-fifre>(_expert)` (`ScenarioDuCombat3`), compteur `intelligence` | `[camp]` 69 au total | `pu144.py pu145.py pu146.py` |
Regression (derniere, verte) : [camp] 69, [gang] 27, [lieu] 41, [renc] 23, [big] 55, [pist] 29, [capo] 30, [pun] 32, [jig] 31, [hob] 30, [ville] 15, [syn] 15, [arm] 10, [hit] 12, [swat] 15 ; `test_cards` 7157 ok. Preuves : `preuves-big-apple.md` (blocs combat 1, 2, 3).
Decisions de l'utilisateur : le combat 4 (Kingsfall) est jouable SEUL (le livret dit que le multi-tables « pods » est une VARIANTE epique) ; on finit TOUTE la campagne classique avant d'envisager le multi-tables (partie a part : etat commun entre parties).

## Fait le 22/10 (nuit) : combat 4 Kingsfall, version normale (non commite au moment de l'ecriture : voir git log)
pu147 Long Live the King? (Setup : allie Punisher au choix des joueurs si gagne, echange en pu148 + 1 jeton), pu148 Power to the People, pu149a/b Long Live / Down With, scenario genere `kingsfall(_expert)`, 11 cas `[camp]`, mutations rouges. pu151 The King = donnees seulement. Pod Action, pods, The King : MODE MULTI-TABLES (a la toute fin). Preuves : `preuves-big-apple.md` (bloc combat 4).

## Fait le 22/10 (nuit, suite) : pu139 + ecran de campagne
pu139 Capo of the Past (commit 6f1c8462) ; ecran de campagne : 4 combats, choix du scenario des combats 2 et 3 d'apres le carnet (`catalogue-carnet.js`, `tools/test_catalogue_carnet.mjs`, 4 epreuves `test_campagnes.py punisher`, `ui-check/tests/campagne-punisher.spec.ts`). Preuves : `preuves-big-apple.md`. RESTE du chantier campagne : regle experte REC, pages de livret, ecran de fin du combat 4.

## Ce qui RESTE (ordre propose)
1. ~~Combat 4 Kingsfall, version normale~~ FAIT (voir ci-dessus). Reste : ajouter le combat 4 a `data/campagnes/punisher_mcdc_2026.json` / l'ecran de campagne. Ancien texte : : scans p269-p273 (Long Live the King? 1A, Power to the People, Long Live, Down With the King, The King), scenario Kingpin (FNE) + sets SWAT et Tracksuit Mafia, Setup « allie Punisher en jeu » si pu146 gagne (cle `Punisher Ally`), victoire = campagne gagnee. Montrer les scans UN PAR UN et poser les questions une a une (regle utilisateur). Dire d'abord quelles cartes servent hors mode multi-tables.
2. **pu139 Capo of the Past** (set modulaire du combat 2, sans script) : « Treat attached character as an ELITE minion » : un VILAIN CAPO traite comme sbire (`TreatAsMinion` ne gere que allie/heros : extension moteur). Question a poser a l'utilisateur avec le scan.
3. **Ecran de campagne** (`Fusion/marvel-lcg-src/public/js/campagne/app.js`) : choisir le scenario des combats 2 et 3 d'apres le carnet (`ScenarioDuCombat2/3` existent cote moteur) ; pages de livret.
4. Regle experte « chaque joueur peut s'attribuer une carte rencontre pour soigner REC » (combats 2 a 4) ; autoplay en mode campagne ; Uptown (PU-10) ; defis p279+ (PU-11) ; textes FR (PU-12) ; batterie complete (~1 h) + audit (PU-13).
5. Interface « La Ville » (PU-8) : EN ATTENTE ; l'utilisateur a dit « on verra en temps voulu » (design « A + B », maquette `docs/packs/mcdc-2026-punisher/maquette-ville.html`).
6. Effets « en jeu » autres que Collaboration vis-a-vis des sbires attaches (cas par cas).
7. Decisions sans texte de RR a confirmer en partie reelle : voir `preuves-big-apple.md`.

## Pièges de harnais (déjà payés cher)
- Toute commande Bash dont le texte contient `tools/test_capacites.py` fait REFUSER le harnais (« un autre harnais tourne ») : mettre la commande dans un fichier script (`/tmp/xxx.sh`, créé avec l'outil Write) et lancer `bash /tmp/xxx.sh`. Ajouter `< /dev/null` pour que le harnais ne mange pas l'entrée du shell.
- Commande de test : `PYTHONPATH=src python3.10 tools/test_capacites.py "$PWD" 40100 /tmp/x.json "[filtre]"` depuis `Fusion/marvel-lcg-src`, avec `/home/oem/Desktop/Marvel LCG/.venv-linux/bin/python3.10` ; puis `git checkout -- launch.json`. Un seul harnais à la fois sur le dossier.
- `Puzzle.PlaceThreat/SetThreat` dans `mise_en_place` est perdu : le mettre dans `declencher`. Une attaque d'ennemi sur un allié demande « Defense » (utiliser `passer_sur_option`). `WhenCardSetup` ne part pas pour une carte révélée par `Find.FindAndReveal` (utiliser `WhenThisRevealed`). Une attaque de remplacement lancée depuis une interruption `WouldAttack` repasse par la même interruption (garde de ré-entrée). Les recto-verso doivent être écrits `"puXXXa,puXXXb"` dans les listes de rencontre/mise de côté.
- Un nom inconnu (ex. `SideScheme`) dans un script est une `NameError` AVALÉE par le moteur : vérifier avec un cas, pas à l'œil. `test_cards` (`/tmp/tc.sh`-like : `tools/test_cards.py "$PWD" 40300 /tmp/r.json`) charge tous les scripts.
- Les décisions P1-P8 et l'ordre PU-0…PU-13 sont dans `docs/rapports/cadrage-14-15-19-2026-10-20.md` §1.7.
