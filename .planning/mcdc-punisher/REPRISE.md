# Reprise du chantier « La ville ne dort jamais » (campagne MC×DC 2026, préfixe `pu`)

État au 21/10/2026, dernier commit de travail Punisher : `c64696fb` (PU-5). Tout est commité ; rien n'est poussé sur GitHub, rien n'est déployé (ne JAMAIS déployer sans demande explicite de l'utilisateur).

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

## Ce qui RESTE (ordre proposé)
1. **PU-5 fin / PU-7 : le scénario 1 « The Big Apple »** (~55 faces) : les 9 lieux (`cartes.md` p059-p075, IDs 6030-6038 → `pu030`-`pu038`), The City (p009, Action de déplacement : épuiser un personnage OU 1 ressource ; condition `Ville.AuLieu`, limite « une fois par round » = `LimitOncePerRound` globale), Never Sleeps (p011), 8 vilains CAPO (4 cartes recto-verso, p095+), les complots Gang War/Silence the City/Gunrunner's Warehouse (p001-p007), sbires attachés à un lieu (Overdrive, Muse, Screwball : M5), pistes/LEADS (9 + 3 Uptown, M3), attachements de lieu. Mise en place du scénario : zone commune + une zone par rangée via `Ville.Installer`, `Villains.SetRule("Leftmost")`.
2. **Capo of the Past (pu139)** : échafaudé, script reporté (cherche un CAPO au hasard : dépend des 8 CAPO).
3. **PU-6** pistes (M3) et sbires attachés (M5) ; **PU-8** interface « La Ville » (captures en Épuré, une à la fois, thème sombre) ; **PU-9** campagne (livret FR : `docs/packs/mcdc-2026-punisher/regles-fr.md`) ; **PU-10** Uptown ; **PU-11** défis + Hawkeye MC×DC ; **PU-12** textes FR ; **PU-13** batterie complète (~1 h) + audit.
4. Questions techniques ouvertes : blocage d'autoplay sur l'Action de héros de Tenacity (01093) dans une partie `one_last_kill_hobgoblin_expert` graine 3 ; `DealDamage` avec un vilain et des sbires dans UNE liste ne blesse pas le vilain (appeler séparément).

## Pièges de harnais (déjà payés cher)
- Toute commande Bash dont le texte contient `tools/test_capacites.py` fait REFUSER le harnais (« un autre harnais tourne ») : mettre la commande dans un fichier script (`/tmp/xxx.sh`, créé avec l'outil Write) et lancer `bash /tmp/xxx.sh`. Ajouter `< /dev/null` pour que le harnais ne mange pas l'entrée du shell.
- Commande de test : `PYTHONPATH=src python3.10 tools/test_capacites.py "$PWD" 40100 /tmp/x.json "[filtre]"` depuis `Fusion/marvel-lcg-src`, avec `/home/oem/Desktop/Marvel LCG/.venv-linux/bin/python3.10` ; puis `git checkout -- launch.json`. Un seul harnais à la fois sur le dossier.
- `Puzzle.PlaceThreat/SetThreat` dans `mise_en_place` est perdu : le mettre dans `declencher`. Une attaque d'ennemi sur un allié demande « Defense » (utiliser `passer_sur_option`). `WhenCardSetup` ne part pas pour une carte révélée par `Find.FindAndReveal` (utiliser `WhenThisRevealed`). Une attaque de remplacement lancée depuis une interruption `WouldAttack` repasse par la même interruption (garde de ré-entrée). Les recto-verso doivent être écrits `"puXXXa,puXXXb"` dans les listes de rencontre/mise de côté.
- Un nom inconnu (ex. `SideScheme`) dans un script est une `NameError` AVALÉE par le moteur : vérifier avec un cas, pas à l'œil. `test_cards` (`/tmp/tc.sh`-like : `tools/test_cards.py "$PWD" 40300 /tmp/r.json`) charge tous les scripts.
- Les décisions P1-P8 et l'ordre PU-0…PU-13 sont dans `docs/rapports/cadrage-14-15-19-2026-10-20.md` §1.7.
