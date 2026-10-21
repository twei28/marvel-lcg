# Spec des briques M1 (lieux) et M2 (territoires) : « La ville ne dort jamais », scénario 1 The Big Apple

21/10/2026. Écrite AVANT le code (cadrage 20/10, §1.7 : M2 est la brique la plus risquée). Sources : livret FR (`la-ville-ne-dort-jamais-regles-fr-v1.txt`, p. 1-3 et FAQ), `cartes.md` (The City p009, Never Sleeps p011, 9 lieux, 9 pistes, Uptown).
Statut : spec de travail, **pas encore relue** par un second regard (le cadrage le demande avant PU-5).

## 1. Ce que disent les règles (lu dans le livret, pas déduit)

| # | Règle | Source |
|---|---|---|
| R1 | 9 lieux en grille 3×3, l'ordre reflète la géographie ; chaque joueur a un marqueur de position, tous partent de Midtown (case 5) | livret p.1-2 |
| R2 | Déplacement orthogonal (↔ ou ↕) par l'**Action** de l'environnement *The City* : épuiser un personnage qu'on contrôle OU dépenser 1 ressource ; autant de fois qu'on peut payer (pas de limite par round) | p009, FAQ |
| R3 | On n'interagit qu'avec les lieux **qu'on occupe** (leurs capacités et les cartes attachées) | p009, FAQ |
| R4 | Chaque **ligne** = le territoire d'un CAPO ; chaque territoire est une zone de jeu distincte | livret p.2 |
| R5 | Pas d'interaction entre joueurs de territoires différents, y compris avec leurs aires de jeu (dont les sbires engagés) | livret p.2, p011 |
| R6 | Un méchant s'active seulement contre les joueurs de SON territoire ; « le méchant » dans une carte = le méchant du territoire du joueur qui résout l'effet | livret p.2 |
| R7 | **Toutes les manigances** (principale et annexes) et les icônes accélération, aléas, amplification, crise n'appartiennent à aucun territoire : leurs effets valent pour tous, tous peuvent les attaquer | livret p.2, p011 |
| R8 | Les capacités des cartes **rencontre** ne sont pas limitées à un territoire (ex. Collaboration compte les sbires de tous les territoires) | FAQ |
| R9 | « Lieu inoccupé » = sans aucun joueur ; un sbire attaché à un lieu s'engage dès qu'un joueur y arrive, les autres du territoire peuvent alors interagir | FAQ |
| R10 | Une capacité de lieu « limite une fois par round » = une fois par round **au total**, pas par joueur | FAQ |
| R11 | À la révélation de 3A, les lieux sont retirés ; un sbire qui tente de s'attacher à un lieu inexistant reste avec le joueur engagé ; tous les CAPO hors jeu sont mis de côté | FAQ |
| R12 | Mise en place : 3 CAPO tirés au hasard parmi 8 (4 avec Uptown : 3 lieux de plus au-dessus de la grille, 3 pistes de plus) ; face A standard, B expert | livret p.1-2 |

## 2. Ce que le moteur sait déjà (références vérifiées dans le code)

- **Une carte a une zone de jeu** (`card.game_area`). `GameArea.AddPlayer(player)` déplace le joueur ET tout ce qu'il possède (personnages, soutiens, sbires engagés, deck, main…) vers la zone et y ajoute les manigances annexes de l'ancienne zone (`game/world/game_area/game_area.py`).
- **Presque tous les filtres de ciblage lisent la zone de la carte qui résout** : `Worlds.GetMainSchemes/GetSideSchemes/GetOnFieldEnemies…(effet)` filtrent par zone (`game/operate/worlds.py:139-160`). C'est le mécanisme dont R4, R5, R6 ont besoin.
- **« Le méchant » est déjà par zone** : `Worlds.FindVillain(effet)` → `Scenario.GetVillain(zone, effet)` (`worlds.py:~190`). R6 demande la même chose qu'aujourd'hui, avec une zone par rangée.
- **Le mode compétitif** (livret mc56) fait déjà d'un camp une zone, avec phases par camp et filtrage des complots, manigances, sbires et deck (`game/world/world.py:184-260`). Les zones multiples sont donc éprouvées.
- **Kang** crée une zone supplémentaire en cours de partie (`toafk/kang/__init__.py:97-112`), mais ne déplace un joueur qu'une fois.
- **Briques du 20/10** : `Enemy.AttackCharacter` (un ennemi attaque un ennemi/allié, `players_may_defend`, `overkill_to`), `Villains` (plusieurs vilains, règle « le méchant »), `CannotBeAffectedByPlayerCards`. Elles servent déjà au scénario 3 (set Punishment, 32 cas verts).

## 3. Ce qui manque (écarts G1 à G9) et la décision pour chacun

| # | Manque | Décision |
|---|---|---|
| G1 | Les manigances doivent être **communes** à toutes les zones (R7) alors que `GetMainSchemes` filtre par zone | Ajouter une **zone commune** réservée (`world.game_area_commune`, créée seulement par le scénario) ; quand elle existe, `GetMainSchemes/GetSideSchemes/GetOnFieldSchemes` y ajoutent ses cartes pour TOUTE zone. Sans zone commune : comportement inchangé (garde pour ~250 scripts) |
| G2 | Les icônes accélération/aléas/amplification/crise doivent compter pour tous (R7) | Elles suivent les manigances : si les manigances sont dans la zone commune, vérifier que `Worlds.GetIconsNum` les compte pour chaque zone ; sinon l'étendre au même garde |
| G3 | Le deck rencontre et la défausse doivent être **uniques** (R8) | **Déjà le cas** : un vilain mis en jeu prend le deck rencontre du scénario (`villain.py:64-71`, `SetEncounterDeck(scenario.encounter_deck)`) et `Worlds.GetEncounterDeck` retombe sur celui du scénario. À confirmer par un cas : deux capos en jeu piochent le même deck |
| G4 | Un joueur doit **changer de zone plusieurs fois** (R2) ; `AddCard` a `assert card.game_area != self` et `AddPlayer` embarque les manigances annexes de l'ancienne zone | Nouvelle fonction `World.MovePlayerToGameArea(joueur, zone)` : retire l'assert pour ce chemin, N'EMBARQUE PAS les cartes de la zone commune, envoie `OnLeaveGameArea` / `OnEnterGameArea` |
| G5 | Les sbires **engagés** suivent-ils le joueur qui change de rangée ? Le livret : « pas d'interaction entre territoires, y compris les sbires dans les aires de jeu » | Ils **restent avec le joueur** (ils sont dans son aire de jeu : `AddPlayer` les emmène déjà) ; c'est la lecture du livret p.2. Cas test dédié |
| G6 | Phase du vilain : chaque capo s'active contre les joueurs de sa zone seulement (R6) | Crochet `GettingVillainsToActivate` (brique du 16/10) déjà prévu pour plusieurs vilains ; à brancher par zone du joueur (`Villains.Rule` ne suffit pas : « le méchant » dépend de la zone) |
| G7 | **Position et lieu** (R1, R3) : aucun état de position n'existe | Chaque lieu = carte `Environment` à trait LOCATION posée dans la zone de SA rangée ; la position d'un joueur = (rangée, colonne) dans le store du monde (`Stores`), recopiée dans un attribut lisible par les conditions (« je suis à Soho ») |
| G8 | « Interagir seulement avec le lieu qu'on occupe » (R3) | Les capacités de lieu (Action, Hero Action, Interrupt…) reçoivent une condition « le joueur qui la déclenche occupe ce lieu » posée par une fabrique `AbilityFactory.AtLocation(...)` ; les cartes attachées à un lieu (M5) vérifient la même condition |
| G9 | Limites « une fois par round » **au total** (R10) | `LimitOncePerRound` existe ; confirmer qu'elle est globale et non par joueur (cas test) |

## 4. Architecture retenue

**Territoires = zones de jeu du moteur** (pas une couche de filtres posée par-dessus). Raison : R4/R5/R6 sont déjà ce que fait le filtrage par zone, et le mode compétitif l'a éprouvé ; une couche de filtres obligerait à toucher chaque appel de ciblage. Le coût est concentré dans G1-G4 (zone commune, partage du deck, déplacement répété).

Schéma : `game_areas[0]` = zone commune (manigances, deck rencontre, défausse, pistes, environnements *The City* / *Never Sleeps*, cartes de lieu attachées ?) ; `game_areas[1..3 ou 4]` = une rangée chacune, avec son CAPO, les joueurs qui y sont, leurs sbires engagés.
Les 9 lieux : chaque carte de lieu est dans la zone de sa rangée (pour que « les cartes attachées au lieu » et « les joueurs ici » suivent la zone).

## 5. Cas limites à tester AVANT l'interface (une ligne = un cas `[ville]`)

1. Départ : tous à Midtown (rangée du milieu, case 5), même zone.
2. Déplacement ↕ vers un autre CAPO : le joueur quitte la zone, entre dans la nouvelle, ses sbires engagés le suivent, ses alliés/soutiens aussi.
3. Déplacement ↔ dans la même rangée : la zone ne change pas.
4. Déplacement en diagonale ou hors grille : refusé.
5. Coût : épuiser un personnage OU 1 ressource ; deux déplacements dans le même round si deux coûts payés.
6. Deux joueurs dans des rangées différentes : l'un ne peut ni défendre, ni contrer un sbire, ni cibler l'allié de l'autre.
7. Phase du vilain : chaque capo n'active que contre les joueurs de sa rangée ; une rangée sans joueur : son capo ne fait rien.
8. « Le méchant » (carte rencontre ou joueur) = le capo de la zone du joueur qui résout.
9. Une manigance est attaquable depuis n'importe quelle rangée ; la menace posée par un capo va sur la manigance commune.
10. Les icônes d'accélération des manigances comptent pour toutes les zones.
11. Collaboration : un sbire révélé dans une zone déclenche l'activation si un sbire MAGGIA est dans une autre.
12. Une capacité de lieu « une fois par round » utilisée par un joueur est épuisée pour l'autre.
13. Sbire attaché à un lieu inoccupé (M5) : il s'engage quand le premier joueur arrive ; avant, personne du territoire ne peut l'attaquer.
14. Lieux retirés (3A) : le sbire qui veut s'attacher reste engagé.
15. Défaite d'un capo : sa zone reste (autres capos) ; fin de partie selon la manigance (pas selon les capos).
16. Uptown : une 4e rangée au-dessus, une 4e zone ; les 3 pistes en plus.

## 6. Ordre de travail proposé (PU-5, 5 étapes, chaque étape testée avant la suivante)

1. **Banc de zones** : harnais `Puzzle` pour créer N zones, y placer des joueurs et des cartes, et vérifier G1-G4 SANS aucune carte de la campagne (cas 2, 3, 6, 9, 10).
2. **Zone commune + garde** dans `Worlds` (G1/G2/G3), avec une batterie complète avant/après pour prouver « aucun changement hors scénario » (la batterie totale dure ~1 h).
3. **Position et déplacement** (G4/G7) : `MovePlayerToGameArea`, le store de position, l'Action de *The City* (cas 1, 2, 3, 4, 5).
4. **Lieux** (G8/G9) : les 9 cartes (texte lu sur scan), la fabrique `AtLocation`, les limites par round (cas 12).
5. **CAPO et phase du vilain** (G6, cas 7, 8, 15) puis les cartes du scénario 1 (22 + 9 + 16 faces) en PU-7.

## 7. Risques et ce que je ne sais pas encore

- **Le risque principal** devient G1 (manigances communes à toutes les zones) : tout ce qui lit `GetMainSchemes(zone)` ou `GetSideSchemes(zone)` (~250 scripts via les filtres) doit rester inchangé sans zone commune, d'où le garde et la batterie avant/après. Le partage du deck rencontre (G3) est, lui, déjà acquis (`villain.py:64-71`).
- **`GetIconsNum` et le calcul de menace** : non lus ; si ils filtrent par zone, G2 est plus gros que prévu.
- **L'interface** (PU-8) dépend de l'état « position + zone » ; les captures viendront après l'étape 3.
- Questions de règle : aucune ouverte, le livret FR répond aux cas de la FAQ ; les cas non couverts (ex. un capo vaincu pendant que des joueurs sont dans sa rangée) seront tranchés par la RR et notés.
