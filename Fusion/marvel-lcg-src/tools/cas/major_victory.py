# Cas test_capacites du heros MAJOR VICTORY (Vance Astro, Gardiens de la Galaxie, prefixe `mv`) : 31 cas, noms commencant par le card_id
# (substituer_pack.py filtre dessus : `tools/substituer_pack.py <game_dir> <port> mv0`).
#
# Rappels de montage :
#  - le deck `major_victory` demarre en ALTER EGO (mv001b) ; `Puzzle.ChangeToFace('mv001b', 'mv001a')` le passe en HEROS ;
#  - Rhino 01094 est le vilain, 01097b son complot principal (⚠ SEUIL : 8 menaces ACCOMPLISSENT le complot et terminent la partie, utiliser 6 au plus),
#    01172 Whiplash a Retaliate 1, 01102 Sandman ATQ 3 ;
#  - `Puzzle.Boost(carte)` ACTIVE le vilain (il attaque en forme heros, manigance en alter-ego) : ne pas y ajouter `Puzzle.Attack` ;
#  - un surge ou un boost revele une AUTRE carte rencontre : `Puzzle.EmptyEncounterDeck()` pour isoler la carte mesuree ;
#  - une attaque REPARTIE (`canbe_divided`) fait 1 degat PAR CHOIX de cible : `cibles` doit lister la cible autant de fois que de points d'ATQ ;
#  - `declencher_tolerant` pour la seconde activation d'une capacite limitee (le refus est ce qu'on mesure).
CAS = [
    # ------------------------------------------------------------------ major_victory (mv) : 30/10/2026
    {
        "nom": "mv006 Psychokinetic Blast — 6 degats et l'ennemi desoriente",
        "pourquoi": ("modele 30007 Swinging Web Pig (texte identique) : `DealDamage(effect.targets, 6)` puis "
                     "`GiveStatus(..., 'Confused')` sur LA MEME cible. Cout 3 paye par trois cartes de la main"),
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": ["Puzzle.ChangeToFace('mv001b', 'mv001a')"],
        "main_exclusive": ["mv006", "mv002", "mv003", "mv004"],
        "declencher": [],
        "jouer": ["mv006"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats_min": [["01094", 6]],
                    "statuts": [["01094", "Confused"]],
                    "defausse": ["mv006"]},
    },
    {
        "nom": "mv008 Psychic Link — 5 menaces retirees et une carte piochee (heros GUARDIAN)",
        "pourquoi": ("modele 04049 Clear the Area : `RemoveThreatFromSchemes(.., 5)` puis `DrawUp(1)` pour chaque joueur "
                     "qui controle un personnage GUARDIAN. Major Victory (face heros) porte le trait. "
                     "Principale a 6 -> 1 (⚠ pas 8 : 8 depasse le seuil de la principale, elle est ACCOMPLIE et la partie "
                     "s'arrete avant que la carte soit jouee) ; main : 4 cartes - Psychic Link - 3 de cout + 1 pioche = 1"),
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": ["Puzzle.ChangeToFace('mv001b', 'mv001a')",
                          "Puzzle.SetThreat('01097b', 6)"],
        "main_exclusive": ["mv008", "mv002", "mv003", "mv004"],
        "declencher": [],
        "jouer": ["mv008"],
        "cibles": ["01097b"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 1]],
                    "taille_main": 1,
                    "defausse": ["mv008"]},
    },
    {
        "nom": "mv005 Shield Block — le bouclier s'incline et TOUS les degats sont evites",
        "pourquoi": ("modele 03005 Shield Block + sr006 (`Identity`) : `HeroInterrupt` sur `WhenUnitWouldTakeDamage`, cout "
                     "`Exhaust(card_type=Upgrade, name=..)`. ⚠ L'ATTAQUANT EST SANDMAN (01102, ATQ 3) : avec DEF 2 il reste "
                     "1 degat, donc « would take any amount of damage » est atteint (lecon dd006). Depuis le script de mv002 (+1 DEF) Sandman ne "
                     "traverse plus : le degat vient de mv015 (3 degats INDIRECTS, Future absente), que Shield Block doit annuler"),
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": ["Puzzle.ChangeToFace('mv001b', 'mv001a')",
                          "Puzzle.PutIntoPlay('mv002', under_control=True)"],
        "main_exclusive": ["mv005"],
        "declencher": ["Puzzle.Reveal('mv015')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0,
                    "exhausted": ["mv002"],
                    "defausse": ["mv005"]},
    },
    {
        "nom": "mv009 Victory's Command — +2 a l'attaque de base, le personnage est redresse, le bouclier incline",
        "pourquoi": ("modele 49019 You Got This! (`WhenUnitUseBasicPower`, `Faces.ReadyAll([message.trigger])`) avec "
                     "`message.GainValue(2)`. Attaque de base de Major Victory : ATQ 1 + 2 = 3 degats. Sandman est la cible "
                     "(pas de Tenacite)"),
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": ["Puzzle.ChangeToFace('mv001b', 'mv001a')",
                          "Puzzle.PutIntoPlay('mv002', under_control=True)"],
        "main_exclusive": ["mv009", "mv003"],
        "cibles": ["01094"],
        "declencher": ["Puzzle.Attack('mv001a')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_min": [["01094", 3]],
                    "pret": ["mv001a"],
                    "exhausted": ["mv002"],
                    "defausse": ["mv009"]},
    },
    {
        "nom": "mv001a Shield Toss — le bouclier du DECK remonte en main, sans degats",
        "pourquoi": ("modele 04001b Weapon of Choice (`Search.PlayerCard` + `GainCard`, `SetCost(Cost('1'))`). Le bouclier "
                     "vient du deck : « if it leaves play this way » est faux, aucun degat"),
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": ["Puzzle.ChangeToFace('mv001b', 'mv001a')",
                          "Puzzle.PutIntoDeck('mv002')"],
        "main_exclusive": ["mv003"],
        "declencher": ["Puzzle.Action('mv001a', 'Action')"],
        "verifier": "etat_attendu",
        "attendu": {"en_main": ["mv002"]},
    },
    {
        "nom": "mv001a Shield Toss — le bouclier EN JEU retourne en main et inflige 4 degats",
        "pourquoi": ("« if it leaves play this way, deal 4 damage to an enemy » : `IsInPlay()` lu AVANT `ReturnToHand`. "
                     "Rhino est la seule cible : elle part d'office"),
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": ["Puzzle.ChangeToFace('mv001b', 'mv001a')",
                          "Puzzle.PutIntoPlay('mv002', under_control=True)"],
        "main_exclusive": ["mv003"],
        "declencher": ["Puzzle.Action('mv001a', 'Action')"],
        "verifier": "etat_attendu",
        "attendu": {"en_main": ["mv002"],
                    "degats_min": [["01094", 4]]},
    },
    {
        "nom": "mv001a Shield Toss — TEMOIN D'EPUISEMENT : une seule fois par round",
        "pourquoi": ("« Limit once per round » : on relance Shield Toss dans le MEME round apres avoir remis le bouclier en "
                     "jeu. Le second declenchement doit etre refuse : le bouclier reste en jeu et Rhino ne prend que les 4 "
                     "premiers degats"),
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": ["Puzzle.ChangeToFace('mv001b', 'mv001a')",
                          "Puzzle.PutIntoPlay('mv002', under_control=True)"],
        "main_exclusive": ["mv003", "mv004"],
        "declencher": ["Puzzle.Action('mv001a', 'Action')",
                       "Puzzle.PutIntoPlay('mv002', under_control=True)"],
        "declencher_tolerant": ["Puzzle.Action('mv001a', 'Action')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["mv002"],
                    "degats": [["01094", 4]]},
    },
    {
        "nom": "mv007 Telekinetic Throw — Shield Toss declenche l'interruption : 4 + 4 degats en plus",
        "pourquoi": ("modele sf006 (`WhenUnitWouldTakeDamage` filtre sur `message.by_effect`, ici le NOM de la capacite). "
                     "Arbitrage utilisateur du 30/10/2026 : deux choix independants (meme cible possible). Shield Toss "
                     "inflige 4 a Rhino, l'interruption en ajoute 4 + 4 : 12 au total, et Major Victory s'incline"),
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": ["Puzzle.ChangeToFace('mv001b', 'mv001a')",
                          "Puzzle.PutIntoPlay('mv002', under_control=True)"],
        "main_exclusive": ["mv007", "mv003", "mv004"],
        "declencher": ["Puzzle.Action('mv001a', 'Action')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_min": [["01094", 12]],
                    "exhausted": ["mv001a"],
                    "defausse": ["mv007"]},
    },
    {
        "nom": "mv002 Captain America's Shield — +1 DEF et retaliate 1 sur Major Victory",
        "pourquoi": ("modele 03009 (`GiveKeywordToAttached(CardFinder(name=..), defense=1, retaliate=1)`). Les DEUX ecarts sont "
                     "mesures : un seul oubli passerait sinon inapercu. Face HEROS (l'alter-ego n'a ni DEF ni retaliate)"),
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": ["Puzzle.ChangeToFace('mv001b', 'mv001a')"],
        "declencher": ["Puzzle.PutIntoPlay('mv002')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"defense": 1, "retaliate": 1}, "en_jeu": ["mv002"]},
    },
    {
        "nom": "mv003 Founder of the Guardians — l'identite devient GUARDIAN et gagne +1 PV (face alter-ego, qui n'avait pas le trait)",
        "pourquoi": ("modeles 56120 (`GiveKeywordToInPlayWhenApplyThis(Identity, trait=..)`) et sk113 (`CardFinder2(trait, Friend)`). "
                     "Vance Astro est MUTANT/PSIONIC/SOLDIER : sans la carte il n'est pas GUARDIAN. Avec elle il le devient, "
                     "puis la 2e ligne lui donne +1 PV"),
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": [],
        "declencher": ["Puzzle.PutIntoPlay('mv003')"],
        "verifier": "etat_attendu",
        "attendu": {"traits_de": [["mv001b", "GUARDIAN"]], "attributs": {"health": 1}, "en_jeu": ["mv003"]},
    },
    {
        "nom": "mv004 Containment Suit — +2 PV pour l'identite",
        "pourquoi": "modele 01036 Mark V Armor (`GiveKeywordToAttached(\"You\", health=2, steady=1)`) : l'ecart de PV est mesure",
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": [],
        "declencher": ["Puzzle.PutIntoPlay('mv004')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"health": 2}, "en_jeu": ["mv004"]},
    },
    {
        "nom": "mv004 Containment Suit — l'identite gagne steady (1)",
        "pourquoi": ("« your identity gains steady » : on mesure l'ATTRIBUT `steady` (modele ligne 28003), et non la presence d'un statut : "
                     "un premier statut Stunned RESTE sur la carte, c'est son effet qui demande deux cartes. Mon premier cas "
                     "mesurait le statut : mauvaise mesure, pas un defaut de la carte"),
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": [],
        "declencher": ["Puzzle.PutIntoPlay('mv004')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"steady": 1}, "en_jeu": ["mv004"]},
    },
    {
        "nom": "mv010 The Captain America — la ressource wild paie une carte pour un joueur qui controle un GUARDIAN",
        "pourquoi": ("modeles 32020 The X-Jet + 16142 Milano (`AnyPlayerCanDoThis`). Founder of the Guardians coute 2 et la main ne "
                     "porte qu'UNE ressource (Containment Suit, energie) : sans le vaisseau elle ne peut pas etre payee. Face "
                     "HEROS = GUARDIAN"),
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": ["Puzzle.ChangeToFace('mv001b', 'mv001a')",
                          "Puzzle.PutIntoPlay('mv010', under_control=True)"],
        "main_exclusive": ["mv003", "mv004"],
        "declencher": [],
        "jouer": ["mv003"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["mv010"], "en_jeu": ["mv003"]},
    },
    {
        "nom": "mv010 The Captain America — TEMOIN : en alter-ego (Vance n'est pas GUARDIAN) le vaisseau ne produit rien",
        "pourquoi": ("meme position, mais en alter-ego : Vance Astro n'a pas le trait GUARDIAN et ne controle aucun personnage qui "
                     "l'ait. La condition `ControleUnGardien` doit refuser : Founder reste en main et le vaisseau pret"),
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": ["Puzzle.PutIntoPlay('mv010', under_control=True)"],
        "main_exclusive": ["mv003", "mv004"],
        "declencher": [],
        "jouer": ["mv003"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["mv010"], "en_main": ["mv003"]},
    },
    {
        "nom": "mv011 Nikki — ses attaques sont a distance : la riposte de Whiplash est ignoree",
        "pourquoi": ("modele 17013 Yondu (`UnitAttackGainKeyword(\"This\", ranged=True)`). Whiplash (01172) a Retaliate 1. Nikki (ATK 2*) "
                     "ne subit QUE le degat consequent de sa propre attaque : 1. Sans `ranged` la riposte en ajouterait un : 2. "
                     "⚠ « divided » : chaque CHOIX de cible fait 1 degat (`damage = 1` par cible, can_attack.py) ; ATQ 2 = 2 choix, "
                     "ici deux fois Whiplash. Un seul choix (le defaut du pilote) ne fait donc que 1 : c'etait le premier echec de ce cas"),
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": ["Puzzle.ChangeToFace('mv001b', 'mv001a')",
                          "Puzzle.PutIntoPlay('mv011', under_control=True)",
                          "Puzzle.PutIntoPlay('01172')"],
        "main_exclusive": ["mv003"],
        "cibles": ["01172", "01172"],
        "declencher": ["Puzzle.Attack('mv011')"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["mv011", 1]], "degats_min": [["01172", 2]]},
    },
    {
        "nom": "mv011 Nikki — les degats de son attaque se REPARTISSENT entre deux ennemis (1 + 1)",
        "pourquoi": ("modele cd002a (`ThisCanAttack(canbe_divided=True)`). ATQ 2 = deux choix de cible : un sur Whiplash, un sur Rhino. "
                     "Chacun prend 1 : c'est la preuve de la repartition, qu'un coup unique de 2 ne montrerait pas"),
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": ["Puzzle.ChangeToFace('mv001b', 'mv001a')",
                          "Puzzle.PutIntoPlay('mv011', under_control=True)",
                          "Puzzle.PutIntoPlay('01172')"],
        "main_exclusive": ["mv003"],
        "cibles": ["01172", "01094"],
        "declencher": ["Puzzle.Attack('mv011')"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01172", 1], ["01094", 1]]},
    },
    {
        "nom": "mv001b Tactical Foresight — le joueur pioche 2 cartes puis remet 1 carte de sa main sur son deck",
        "pourquoi": ("modeles lj009 (`SetTarget(\"Players\")`) et bw001b (`MoveAllToDeck(.., \"Top\", ..)`). Main : 1 carte + 2 piochees - 1 "
                     "replacee = 2. La carte replacee est la PREMIERE de la main (le pilote choisit toujours la premiere)"),
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": [],
        "main_exclusive": ["mv003"],
        "declencher": ["Puzzle.Action('mv001b', 'Action')"],
        "verifier": "etat_attendu",
        "attendu": {"taille_main": 2},
    },
    {
        "nom": "mv001b Tactical Foresight — TEMOIN D'EPUISEMENT : une seule fois par round",
        "pourquoi": ("« Limit once per round » : on relance l'Action dans le MEME round. Le second declenchement doit etre refuse : "
                     "la main reste a 2 cartes au lieu de 3 (+2 piochees -1 replacee)"),
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": [],
        "main_exclusive": ["mv003"],
        "declencher": ["Puzzle.Action('mv001b', 'Action')"],
        "declencher_tolerant": ["Puzzle.Action('mv001b', 'Action')"],
        "verifier": "etat_attendu",
        "attendu": {"taille_main": 2},
    },
    {
        "nom": "mv013 Michael Korvac — a la revelation, il cherche Korvac's Future et la revele",
        "pourquoi": ("modele 21177 Enchantress (`Search.EncounterCard(.., include_discard_pile=True, include_set_aside=True, name=..)`) "
                     "+ `Reveal`. La Future commence MISE DE COTE : apres la revelation de Korvac elle doit etre EN JEU"),
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": ["Puzzle.ChangeToFace('mv001b', 'mv001a')"],
        "declencher": ["Puzzle.Reveal('mv013')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["mv013", "mv014"]},
    },
    {
        "nom": "mv013 Michael Korvac — tant qu'il est en jeu, la menace de Korvac's Future ne peut pas etre retiree",
        "pourquoi": ("modele 10027 Total Destruction (`ThreatCannotBeRemovedFromWhile`). Korvac et la Future en jeu, 4 menaces ; "
                     "Psychic Link veut en retirer 5 : la Future doit RESTER a 4"),
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": ["Puzzle.ChangeToFace('mv001b', 'mv001a')",
                          "Puzzle.PutIntoPlay('mv013')",
                          "Puzzle.PutIntoPlay('mv014')"],
        "main_exclusive": ["mv008", "mv002", "mv003", "mv004"],
        "declencher": [],
        "jouer": ["mv008"],
        "cibles": ["mv014"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["mv014", 4]]},
    },
    {
        "nom": "mv013 Michael Korvac — TEMOIN : sans Korvac en jeu, la menace de la Future PEUT etre retiree",
        "pourquoi": ("la carte est imprimee sur Korvac : sans lui en jeu l'interdiction ne s'applique pas. Meme position, sans Korvac : "
                     "Psychic Link retire 4 menaces (le complot ne peut pas descendre sous 0) et la Future tombe a 0"),
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": ["Puzzle.ChangeToFace('mv001b', 'mv001a')",
                          "Puzzle.PutIntoPlay('mv014')"],
        "main_exclusive": ["mv008", "mv002", "mv003", "mv004"],
        "declencher": [],
        "jouer": ["mv008"],
        "cibles": ["mv014"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["mv014", 0]]},
    },
    {
        "nom": "mv014 Korvac's Future — a 4 menaces ou plus, chaque identite a -1 de taille de main",
        "pourquoi": ("modele st005b / 04165 (`GiveKeywordToInPlayWhenApplyThis(.., hand_size=-1, condition=..)`). Le complot entre avec 4 "
                     "menaces (seuil ATTEINT : « 4 or more », pas « more than 4 »)"),
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": [],
        "declencher": ["Puzzle.PutIntoPlay('mv014')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"hand_size": -1}, "menace": [["mv014", 4]]},
    },
    {
        "nom": "mv014 Korvac's Future — TEMOIN : sous 4 menaces (3), aucun malus de main",
        "pourquoi": "meme position avec 3 menaces : le seuil n'est pas atteint, l'ecart de taille de main doit etre 0",
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": ["Puzzle.PutIntoPlay('mv014')"],
        "declencher": ["Puzzle.SetThreat('mv014', 3)"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"hand_size": 0}, "menace": [["mv014", 3]]},
    },
    {
        "nom": "mv014 Korvac's Future — a 14 menaces les joueurs PERDENT",
        "pourquoi": ("modeles ra029 / wt018 (`AfterSchemePlaceThreat(.., has_at_least_threat=14)` + `Worlds.SetGameOver(False, ..)`). "
                     "4 menaces a l'entree + 10 posees = 14"),
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": ["Puzzle.PutIntoPlay('mv014')"],
        "declencher": ["Puzzle.PlaceThreat('mv014', 10)"],
        "verifier": "gorr_partie_perdue",
    },
    {
        "nom": "mv014 Korvac's Future — TEMOIN : a 13 menaces la partie continue",
        "pourquoi": "seuil « at least 14 » : 4 + 9 = 13 ne perd pas. Sans ce temoin un seuil trop bas passerait inapercu",
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": ["Puzzle.PutIntoPlay('mv014')"],
        "declencher": ["Puzzle.PlaceThreat('mv014', 9)"],
        "verifier": "mv_partie_en_cours",
    },
    {
        "nom": "mv015 Judgment of Korvac — sans Korvac's Future en jeu : 3 degats indirects (seule branche possible)",
        "pourquoi": ("modele mw013 (`identite.TakeIndirectDamage`). La Future est mise de cote : poser 2 menaces dessus est IMPOSSIBLE, "
                     "le joueur subit donc 3 degats indirects et la carte ne gagne PAS de surge"),
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": ["Puzzle.ChangeToFace('mv001b', 'mv001a')"],
        "declencher": ["Puzzle.Reveal('mv015')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 3},
    },
    {
        "nom": "mv015 Judgment of Korvac — avec la Future en jeu, branche MENACE : +2 menaces sur la Future",
        "pourquoi": ("modele mw013 (`ChooseAbilities`) ; arbitrage utilisateur du 30/10/2026 : le surge n'accompagne QUE cette branche. "
                     "Future a 4 menaces + 2 = 6, et l'identite ne subit aucun degat indirect. ⚠ Deck rencontre VIDE : le surge de cette branche "
                     "revele une autre carte, qui infligeait 1 degat a la premiere version du cas (preuve que le surge part)"),
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": ["Puzzle.ChangeToFace('mv001b', 'mv001a')",
                          "Puzzle.PutIntoPlay('mv014')",
                          "Puzzle.EmptyEncounterDeck()"],
        "preferer_option": "Place 2 threat",
        "declencher": ["Puzzle.Reveal('mv015')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["mv014", 6]], "degats_identite": 0},
    },
    {
        "nom": "mv015 Judgment of Korvac — [star] Boost sans Future en jeu : l'attaque de Rhino fait 2 + 3 icones - 2 DEF = 3",
        "pourquoi": ("modele sk113 (`message.GainBoostIcon(2, effect)`). Sans Future en jeu la branche menace est impossible : "
                     "les +2 icones s'appliquent d'office (1 imprimee + 2 = 3). Mesure par les DEGATS SUBIS (la carte boost n'est "
                     "pas « en jeu » pour `icones_boost`). Forme HEROS (DEF 2) : `Puzzle.Boost` ACTIVE le vilain, qui attaque : 2 d'ATQ + 3 icones - 2 "
                     "DEF = 3 degats, contre 1 sans la capacite. ⚠ Deck rencontre VIDE (sinon une autre carte boost s'ajoute) ; ⚠ pas de "
                     "`Puzzle.Attack` en plus : `Boost` active deja le vilain (premieres mesures : 7 puis 2, a cause de ces deux effets)"),
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": ["Puzzle.ChangeToFace('mv001b', 'mv001a')", "Puzzle.EmptyEncounterDeck()"],
        "declencher": ["Puzzle.Boost('mv015')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 3},
    },
    {
        "nom": "mv015 Judgment of Korvac — [star] Boost avec la Future en jeu, branche MENACE : +2 menaces, la carte reste a 1 icone",
        "pourquoi": ("meme position que le cas precedent mais la Future est en jeu et le joueur choisit la menace : elle passe de 4 a 6 "
                     "et l'attaque n'a que 1 icone : 2 d'ATQ + 1 - 2 DEF = 1 degat (contre 3 dans la branche icones). Les DEUX "
                     "ecarts, menace ET degats, sont mesures"),
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": ["Puzzle.ChangeToFace('mv001b', 'mv001a')", "Puzzle.PutIntoPlay('mv014')", "Puzzle.EmptyEncounterDeck()"],
        "preferer_option": "Place 2 threat",
        "declencher": ["Puzzle.Boost('mv015')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["mv014", 6]], "degats_identite": 1},
    },
    {
        "nom": "mv016 Accept Perfection — 1re puce : Korvac est revele et la Future recoit 4 menaces (4 + 4 = 8)",
        "pourquoi": ("modeles 21177 (recherche + `Reveal`) et mw013 (`ChooseAbilities`) ; le pilote prend la PREMIERE branche. Korvac "
                     "est revele (la Future entre en jeu avec 4 menaces) PUIS 4 menaces sont posees : 8"),
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": ["Puzzle.ChangeToFace('mv001b', 'mv001a')"],
        "declencher": ["Puzzle.Reveal('mv016')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["mv013", "mv014"], "menace": [["mv014", 8]]},
    },
    {
        "nom": "mv016 Accept Perfection — 2e puce : la carte de plus haut cout que tu controles est defaussee",
        "pourquoi": ("modele 07042 Oversized Hands (`DiscardControlCards(.., highest_cost=True)`). Nikki (cout 3) et le bouclier (cout 1) "
                     "sont en jeu : seule Nikki part"),
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": ["Puzzle.ChangeToFace('mv001b', 'mv001a')",
                          "Puzzle.PutIntoPlay('mv011', under_control=True)",
                          "Puzzle.PutIntoPlay('mv002', under_control=True)"],
        "preferer_option": "Discard the highest cost",
        "declencher": ["Puzzle.Reveal('mv016')"],
        "verifier": "etat_attendu",
        "attendu": {"defausse": ["mv011"], "en_jeu": ["mv002"]},
    },
    {
        "nom": "mv012 Damaged Containment Suit — Forced Interrupt : toute source de degats en fait 1 de PLUS (3 indirects -> 4)",
        "pourquoi": ("modele dt094 (`WhenUnitWouldTakeDamage` + `message.IncreaseDamage(1)`, identite du porteur). « any amount of damage » : "
                     "PAS de `is_from_attack`. Les 3 degats INDIRECTS de mv015 (Future absente) deviennent 4 ; le cas mv015 sans obligation "
                     "mesure 3, c'est l'ecart qui prouve la carte"),
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": ["Puzzle.PutIntoPlay('mv012', under_control=True)"],
        "declencher": ["Puzzle.Reveal('mv015')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 4},
    },
    {
        "nom": "mv012 Damaged Containment Suit — When Revealed : le Containment Suit du DECK est glisse sous l'obligation",
        "pourquoi": ("modele rg012 Caged Bird (`Search.SearchForCard(.., include_in_play=True, name=..)` + `PlaceCardHere(carte, False, ..)`). "
                     "Le costume est au sommet du deck : apres la revelation il doit etre SOUS mv012 (`pose_sous`), pas en jeu"),
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": ["Puzzle.PutIntoDeck('mv004')"],
        "declencher": ["Puzzle.Reveal('mv012')"],
        "verifier": "etat_attendu",
        "attendu": {"pose_sous": [["mv012", "mv004"]], "taille_pose_sous": [["mv012", 1]]},
    },
    {
        "nom": "mv012 Damaged Containment Suit — When Revealed : le costume PORTE est glisse sous l'obligation et l'identite perd ses +2 PV",
        "pourquoi": ("« Find » couvre aussi le jeu (comme rg012). Vance Astro porte le costume (PV 10 + 2) sans degat : il le perd, son maximum "
                     "retombe a 10 et il n'a AUCUN degat (10 sur 10)"),
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": ["Puzzle.PutIntoPlay('mv004')"],
        "declencher": ["Puzzle.Reveal('mv012')"],
        "verifier": "etat_attendu",
        "attendu": {"pose_sous": [["mv012", "mv004"]], "degats_identite": 0},
    },
    {
        "nom": "mv012 Damaged Containment Suit — PV restants ramenes a 0 ou moins par le depart du costume : le cadran est remis a 1",
        "pourquoi": ("clause « set your hit point dial to 1 instead » (modele 03008 `SetHealth(1)`). Vance Astro a 12 PV avec le costume et "
                     "11 degats : il lui reste 1. Le depart du costume lui retire 2 : sans la clause il tomberait a -1 et serait "
                     "DEFAIT. Avec elle il reste en vie a 1 PV, soit 9 degats sur un maximum de 10"),
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": ["Puzzle.PutIntoPlay('mv004')", "Puzzle.Damage('mv001b', 11)"],
        "declencher": ["Puzzle.Reveal('mv012')"],
        "verifier": "etat_attendu",
        "attendu": {"pose_sous": [["mv012", "mv004"]], "degats_identite": 9},
    },
    {
        "nom": "mv012 Damaged Containment Suit — TEMOIN : si les PV restants restent positifs, ils baissent de 2 sans etre remis a 1",
        "pourquoi": ("meme position avec 5 degats (il reste 7 sur 12) : le depart du costume ramene les PV restants a 5, PAS a 1. Le degat "
                     "reste donc a 5 sur un maximum de 10. Sans ce temoin une clause qui remettrait TOUJOURS a 1 passerait inapercue"),
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": ["Puzzle.PutIntoPlay('mv004')", "Puzzle.Damage('mv001b', 5)"],
        "declencher": ["Puzzle.Reveal('mv012')"],
        "verifier": "etat_attendu",
        "attendu": {"pose_sous": [["mv012", "mv004"]], "degats_identite": 5},
    },
    {
        "nom": "mv012 Damaged Containment Suit — Alter-Ego Action : le costume revient en main, l'obligation quitte le jeu, Vance Astro est incline",
        "pourquoi": ("modele rg012 (`AlterEgoAction` + `Exhaust(\"YourIdentity\")`) ; le costume est remis en main AVANT que l'obligation parte "
                     "(la retirer d'abord l'emporterait avec elle). `hors_jeu` et non `defausse`"),
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": ["Puzzle.PutIntoDeck('mv004')"],
        "declencher": ["Puzzle.Reveal('mv012')", "Puzzle.Action('mv012', 'AlterEgoAction')"],
        "verifier": "etat_attendu",
        "attendu": {"en_main": ["mv004"], "hors_jeu": ["mv012"], "exhausted": ["mv001b"]},
    },
    {
        "nom": "mv009 Victory's Command — branche THWART du heros : +2 au contre de base (2 + 2 = 4), heros redresse, bouclier incline",
        "pourquoi": ("meme carte que la branche ATTAQUE, autre pouvoir : `powers=[\"THW\", \"ATK\"]` couvre les deux et `GainValue` ajoute au pouvoir "
                     "UTILISE. Principale a 6, contre de base 2 + 2 = 4 : il reste 2"),
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": ["Puzzle.ChangeToFace('mv001b', 'mv001a')",
                          "Puzzle.PutIntoPlay('mv002', under_control=True)",
                          "Puzzle.SetThreat('01097b', 6)"],
        "main_exclusive": ["mv009", "mv003"],
        "cibles": ["01097b"],
        "declencher": ["Puzzle.Thwart('mv001a')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 2]], "pret": ["mv001a"], "exhausted": ["mv002"], "defausse": ["mv009"]},
    },
    {
        "nom": "mv009 Victory's Command — sur une ALLIEE (« a friendly character ») : Nikki contre pour 2 + 2 = 4 et est redressee",
        "pourquoi": ("« a friendly CHARACTER » = `Friend` (identite ET allies). Nikki (THW 2**) contre : 2 + 2 = 4 menaces retirees (6 -> 2), "
                     "elle est REDRESSEE malgre le cout d'exhaust du contre, et subit ses 2 degats consequents"),
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": ["Puzzle.ChangeToFace('mv001b', 'mv001a')",
                          "Puzzle.PutIntoPlay('mv011', under_control=True)",
                          "Puzzle.PutIntoPlay('mv002', under_control=True)",
                          "Puzzle.SetThreat('01097b', 6)"],
        "main_exclusive": ["mv009", "mv003"],
        "cibles": ["01097b"],
        "declencher": ["Puzzle.Thwart('mv011')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 2]], "pret": ["mv011"], "exhausted": ["mv002"], "degats": [["mv011", 2]]},
    },
    {
        "nom": "mv003 Founder of the Guardians — une ALLIEE GUARDIAN (Nikki) gagne aussi +1 PV (3 -> 4)",
        "pourquoi": ("« each friendly GUARDIAN CHARACTER » = identite ET allies. Nikki a le trait GUARDIAN imprime : ses PV passent de 3 a 4. "
                     "Mesure sur la CARTE (`attributs_carte`), l'identite etant couverte par le cas precedent. ⚠ `attributs_carte` prend l'ECART par "
                     "rapport au PV imprime (+1), pas la valeur absolue : ma premiere version attendait 4 et lisait « attendu 7 »"),
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": ["Puzzle.ChangeToFace('mv001b', 'mv001a')", "Puzzle.PutIntoPlay('mv011', under_control=True)"],
        "declencher": ["Puzzle.PutIntoPlay('mv003')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["mv011", "health", 1]], "en_jeu": ["mv003"]},
    },
    {
        "nom": "mv015 Judgment of Korvac — SURGE mesure DIRECTEMENT : branche menace, la carte suivante du deck rencontre est revelee",
        "pourquoi": ("arbitrage utilisateur du 30/10/2026 : le surge accompagne la branche menace. Le deck rencontre ne contient qu'un sbire connu "
                     "(01101 Hydra Mercenary) : avec le surge il est REVELE donc en jeu. Mesure directe, au lieu de deduire le surge d'un degat"),
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": ["Puzzle.ChangeToFace('mv001b', 'mv001a')", "Puzzle.PutIntoPlay('mv014')",
                          "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101')"],
        "preferer_option": "Place 2 threat",
        "declencher": ["Puzzle.Reveal('mv015')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["01101"], "menace": [["mv014", 6]]},
    },
    {
        "nom": "mv015 Judgment of Korvac — TEMOIN : branche DEGATS (Future absente), PAS de surge : le sbire reste dans le deck rencontre",
        "pourquoi": ("meme deck rencontre, Future absente : seule la branche degats existe, SANS surge (decision utilisateur). Le sbire 01101 doit "
                     "rester dans le deck rencontre. Sans ce temoin un surge inconditionnel passerait inapercu"),
        "scenario": "rhino",
        "heros": "major_victory",
        "mise_en_place": ["Puzzle.ChangeToFace('mv001b', 'mv001a')", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101')"],
        "declencher": ["Puzzle.Reveal('mv015')"],
        "verifier": "etat_attendu",
        "attendu": {"dans_deck_rencontre": ["01101"], "degats_identite": 3},
    },
]

VERIFICATIONS = r'''
def mv_partie_en_cours(monde, aides):
    """mv014 : a 13 menaces (seuil 14 non atteint) la partie n'est PAS terminee."""
    if monde.is_game_over:
        return False, f"la partie est terminee a tort ({monde.game_over.reason})"
    return True, "partie toujours en cours"
'''
