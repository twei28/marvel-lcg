# Cas test_capacites du scenario custom THE HUNGER CORE (Marvel Zombies, Penasquequeman, prefixe `hg`).
# 1er fichier : le VILAIN (hg001-hg003) seul, monte sur le scenario officiel Rhino (comme les briques communes,
# tools/cas/briques_communes.py) : on n'a pas besoin du Setup custom (hg004a, pas encore ecrit) pour tester les
# capacites PROPRES du Coeur, posees directement avec `Puzzle.PutIntoPlay`.
#
# Rappels de montage :
#  - scenario `rhino`, heros `spider_man` ; `FORME_HEROS` passe en forme heros (Just a Core l'exige) ;
#  - `RIEN_A_BOOSTER` remplace le deck de rencontre par des cartes sans icone boost (comme briques_communes.py) ;
#  - le pilote cible hg001 via `"cibles": ["hg001"]` quand plusieurs ennemis sont en jeu (Rhino 01094 + hg001).

FORME_HEROS = "Puzzle.ChangeForm('01001b')"
RIEN_A_BOOSTER = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105')"]
# Zombie Iron Man (hg008) attache a son entree en jeu une amelioration TIREE AU HASARD de son deck signature
# (hg019-hg022). `IRON_MAN_NU` (a placer juste apres `Puzzle.PutIntoPlay('hg008')`) la retire du jeu pour que
# chaque cas hg019-hg023 parte d'un Iron Man sans aucune amelioration, puis attache EXPLICITEMENT celles qu'il veut.
# Les copies non trouvees en jeu sont creees hors jeu puis retirees aussitot (sans effet).
IRON_MAN_NU = "Puzzle.Remove('hg019', 'hg020', 'hg021', 'hg022')"

CAS = [
    # ============================================================ Shielded by the Horde
    {
        "nom": "[hg] hg001 Shielded by the Horde : un Metazombie en jeu -> l'attaque du heros sur le Coeur est refusee (0 degat)",
        "pourquoi": "« While any Metazombie is in play, The Hunger Core cannot be targeted by player cards or abilities, "
                    "cannot be dealt damage »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg001')", "Puzzle.PutIntoPlay('hg007')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('01001a')"],
        # Le pilote VEUT hg001 : refuse comme cible protegee, l'attaque retombe sur Rhino (seul ennemi ciblable restant).
        "cibles": ["hg001"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["hg001", 0], ["01094", 2]]},
    },
    {
        "nom": "[hg] hg001 exposed : aucun Metazombie en jeu -> le heros peut attaquer et blesser le Coeur normalement",
        "pourquoi": "« When no Metazombie is left, the Core ... can now be targeted, dealt damage »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg001')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('01001a')"],
        "cibles": ["hg001"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["hg001", 2]]},
    },
    {
        "nom": "[hg] hg001 TEMOIN sans bouclier (Rhino, meme montage) : l'attaque passe -> prouve que la question 1 mesure vraiment un refus",
        "pourquoi": "contre-cas : sans Shielded by the Horde (ici Rhino, une cible ordinaire), l'attaque du heros blesse normalement",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('01001a')"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 2]]},
    },

    # ============================================================ Rupture X
    {
        "nom": "[hg] hg001 Rupture 1 : un Metazombie vaincu inflige 1[per_hero] degat direct au Coeur, MEME blinde par un autre Metazombie",
        "pourquoi": "« After a Metazombie is defeated, The Hunger Core takes X damage. This damage ignores Shielded by the Horde. » "
                    "Solo : 1 joueur -> 1 degat. hg008 reste en jeu : le bouclier tient, mais Rupture passe quand meme.",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg001')",
                          "Puzzle.PutIntoPlay('hg007')", "Puzzle.PutIntoPlay('hg008')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Damage('hg007', 99)"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["hg007"], "en_jeu": ["hg008"], "degats": [["hg001", 1]]},
    },

    # ============================================================ Just a Core X
    {
        "nom": "[hg] hg001 Just a Core 1 : le Coeur expose attaque un heros en FORME HEROS -> 1 carte de rencontre face cachee, 0 degat",
        "pourquoi": "« When it activates against a player in hero form, instead of attacking, that player deals themself X "
                    "facedown encounter cards. » Pas de Metazombie en jeu : Coeur expose, donc attaquable/actif.",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg001')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Activate('hg001')"],
        "verifier": "hg_distribuees_et_pas_de_degats",
        "attendu": {},
    },
    {
        "nom": "[hg] hg001 Just a Core : le Coeur active contre un ALTER-EGO -> manigance normalement (regle de base, rien de custom)",
        "pourquoi": "« Against an alter-ego it schemes as usual. » Contre-cas de la question precedente : la forme change tout.",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('hg001')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Activate('hg001')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0, "menace_min": [["01097b", 1]]},
    },

    # ============================================================ hg002/hg003 : Infection au When Revealed
    {
        "nom": "[hg] hg002 When Revealed : chaque joueur pose 1 compteur Infection",
        "pourquoi": "« When Revealed: Each player places 1 infection counter. » (hg002 et hg003, texte identique)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg002')"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs_identite": [["infection", 1]]},
    },

    # ============================================================ hg007 : Zombie Captain America
    {
        "nom": "[hg] hg007 Leader of the Horde : un AUTRE Metazombie en jeu gagne +1 ATK, hg007 lui-meme N'EN PROFITE PAS",
        "pourquoi": "« Each other Metazombie gets +1 ATK. » Cible hg013 (pas encore script, aucune capacite propre) plutot que hg008 : "
                    "hg008 porte lui-meme une capacite qui s'attache une amelioration a son entree en jeu (+1 ATK en prime), ce qui "
                    "fausserait la mesure de CE buff-ci en ajoutant un second +1 independant.",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('hg007')", "Puzzle.PutIntoPlay('hg013')"],
        "main_exclusive": ["01088"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["hg013", "attack", 1], ["hg007", "attack", 0]]},
    },
    {
        "nom": "[hg] hg007 Shield : le PREMIER degat de la phase est reduit de 2",
        "pourquoi": "« Forced Interrupt: The first time each phase Zombie Captain America would take damage, reduce that damage by 2. »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('hg007')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Damage('hg007', 5)"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["hg007", 3]]},
    },
    {
        "nom": "[hg] hg007 Shield, TEMOIN D'EPUISEMENT : un SECOND degat dans la MEME phase n'est plus reduit (3 + 5 = 8, pas 3 + 3)",
        "pourquoi": "« The FIRST TIME each phase » : la limite doit mordre sur le second coup de la meme phase",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('hg007')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Damage('hg007', 5)", "Puzzle.Damage('hg007', 5)"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["hg007", 8]]},
    },

    # ============================================================ hg008 : Zombie Iron Man
    {
        "nom": "[hg] hg008 Forced Response : a l'entree en jeu, une amelioration de son deck signature s'attache automatiquement -> +1 ATK (Upgrades)",
        "pourquoi": "« After Zombie Iron Man enters play, discard cards from his signature deck until an attachment is discarded and attach it "
                    "to him. » + « Upgrades. ... gets +1 ATK for each attachment on him. » Sur les 5 cartes du deck signature (hg019-hg023), "
                    "4 sont des UPGRADE (hg023 ne l'est pas) : une amelioration est TOUJOURS trouvee en au plus 2 tirages, quel que soit l'ordre "
                    "melange -> la carte precise attachee n'est pas deterministe, seul le COMPTE l'est.",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg008')"],
        "main_exclusive": ["01088"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"taille_attaches": [["hg008", 1]], "attributs_carte": [["hg008", "attack", 1]]},
    },
    {
        "nom": "[hg] hg008 Upgrades, TEMOIN D'ECHELLE : une DEUXIEME amelioration attachee (16149 Power Stone, carte type Attachment comme hg019-hg022) porte le bonus a +2 ATK (+1 de plus, Power Stone, +3 au total)",
        "pourquoi": "« gets +1 ATK FOR EACH attachment on him » : le bonus doit suivre le COMPTE, pas rester fige a +1. « Attachment » designe le TYPE "
                    "de carte (`GetAttachedAttachments` filtre `card_type=Attachment`, modele 04114) : une amelioration JOUEUR (type « Upgrade », "
                    "ex. 01074 Inspired) ne compterait PAS, d'ou le choix d'une vraie carte de type Attachment pour ce temoin. Power Stone (16149) "
                    "porte elle-meme « ATK+1 » imprime (desc native, independant de hg008) : +1 (Power Stone native) + 2 (compte de 2 ameliorations "
                    "x +1 ATK chacune) = +3 au total sur l'ATQ imprimee (1 -> 4).",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg008')", "Puzzle.AttachReel('16149', 'hg008')"],
        "main_exclusive": ["01088"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"taille_attaches": [["hg008", 2]], "attributs_carte": [["hg008", "attack", 3]]},
    },
    {
        "nom": "[hg] hg008 deck signature : les 4 cartes NON attachees restent dans le deck signature (remelangees, pas perdues)",
        "pourquoi": "« Then shuffle the discarded cards into his signature deck » : les cartes ecartees reviennent dans CE deck, "
                    "elles ne disparaissent pas et ne vont pas a la defausse de rencontre",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg008')"],
        "main_exclusive": ["01088"],
        "declencher": [],
        "verifier": "hg008_deck_signature_etat",
        "attendu": {"taille_deck_signature": 4},
    },

    # ============================================================ hg009 : Zombie Hulk
    {
        "nom": "[hg] hg009 Overkill + Devour : attaque l'identite (01002 Black Cat defend, 2 PV) avec 4 ATQ -> l'alliee meurt, "
               "2 degats d'exces a l'identite (Overkill), hg009 soigne 2 (Devour, PV max de l'alliee vaincue)",
        "pourquoi": "« Overkill. » (texte nu, pas de boost : gagne l'exces en PERMANENCE, pas seulement sur une activation) + "
                    "« Devour — Forced Response: After Zombie Hulk defeats an ally, he heals damage equal to that ally's maximum hit points. » "
                    "« l'identite » car c'est un ENNEMI qui abat un allie (mots-cles/overkill.md : l'exces va au controleur, pas au mechant). "
                    "Montage : un ennemi attaque TOUJOURS le joueur (`Puzzle.EnemyAttacks(mechant, identite, defender=allie)`), l'allie "
                    "designe comme DEFENSEUR encaisse les degats a sa place (regle de base, pas de `ally_attack_is_against_player=False`, "
                    "qui sert a un tout autre cas : l'ennemi attaque l'allie SANS passer par le joueur du tout).",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg009')", "Puzzle.PutIntoPlay('01002', under_control=True)",
                          "Puzzle.Damage('hg009', 5)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EnemyAttacks('hg009', '01001b', defender='01002')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["01002"], "degats_identite": 2, "degats": [["hg009", 3]]},
    },
    {
        "nom": "[hg] hg009 TEMOIN : une alliee qui SURVIT (01050 Hulk, 5 PV >= 4 ATQ) -> aucun exces, aucun soin (Devour ne part pas sans defaite)",
        "pourquoi": "contre-cas : sans defaite, ni Overkill (rien a reporter) ni Devour (rien a soigner) ne partent",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg009')", "Puzzle.PutIntoPlay('01050', under_control=True)",
                          "Puzzle.Damage('hg009', 5)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EnemyAttacks('hg009', '01001b', defender='01050')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["01050"], "degats_identite": 0, "degats": [["hg009", 5]]},
    },

    # ============================================================ hg010 : Zombie Spider-Man
    {
        "nom": "[hg] hg010 Web : apres avoir blesse le heros par son attaque, ce heros est etourdi",
        "pourquoi": "« Forced Response: After Zombie Spider-Man deals damage to a hero, that hero is stunned. » "
                    "Attaque non defendue (pas d'allie) : le heros encaisse directement les 2 ATQ imprimes et devient Etourdi.",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg010')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EnemyAttacks('hg010', '01001a')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2, "statuts": [["01001a", "Stunned"]]},
    },
    {
        "nom": "[hg] hg010 Web, contre-cas « a HERO » : l'attaque DEFENDUE par une alliee (01050 Hulk, 5 PV, qui ENCAISSE les degats a sa place "
               "et SURVIT) n'etourdit PAS le heros -- la cible blessee est l'alliee, pas un Hero",
        "pourquoi": "« that hero is stunned » : seulement si la cible BLESSEE est un Hero (desc.Hero, modele 60166 Kingpin's Cane). Une alliee "
                    "qui defend encaisse les degats a la place du joueur (regle de base) : c'est ELLE qui est blessee, pas l'identite en forme "
                    "heros -- ce contre-cas prouve que le filtre `Hero` (pas `Character`/`None`) mord vraiment, sans quoi l'alliee serait etourdie. "
                    "01050 Hulk (5 PV) plutot que 01002 Black Cat (2 PV, deja utilisee par hg009) : elle doit SURVIVRE aux 2 ATQ pour rester "
                    "en jeu et prouver l'absence de statut sur SA carte, pas seulement sur l'identite.",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg010')", "Puzzle.PutIntoPlay('01050', under_control=True)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EnemyAttacks('hg010', '01001a', defender='01050')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0, "degats": [["01050", 2]],
                    "statuts_absents": [["01001a", "Stunned"], ["01050", "Stunned"]]},
    },

    # ============================================================ hg011 : Zombie Captain Marvel
    {
        "nom": "[hg] hg011 Absorption : apres avoir ete attaquee, elle pose 1 compteur energy et gagne +1 ATK",
        "pourquoi": "« Absorption — Forced Response: After she is attacked, place 1 energy counter on this card "
                    "(max. 5). She gets +1 ATK for each energy counter. » Attaque non defendue (pas d'allie) : "
                    "le compteur se pose meme si c'est elle qui blesse le heros, puisque la capacite n'exige ni "
                    "degats ni defense, seulement « apres etre attaquee ».",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg011')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('01001a')"],
        "cibles": ["hg011"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["hg011", "energy", 1]], "attributs_carte": [["hg011", "attack", 1]]},
    },
    {
        "nom": "[hg] hg011 Absorption, TEMOIN D'EPUISEMENT DU PLAFOND : deja a 4 compteurs, DEUX attaques "
               "supplementaires posent la 5e (max.) mais jamais de 6e -> +5 ATK, pas +6",
        "pourquoi": "« (max. 5) » : le plafond est porte par `PlaceCountersOn(..., maximum=5)`. Montage a 4 "
                    "compteurs via `Puzzle.Counter('hg011', 'energy', 4)` (equivalent d'une mise en place "
                    "atteinte par 4 attaques successives, sans risquer que hg011 meure en cours de route), puis "
                    "DEUX attaques de suite declenchent Absorption deux fois : la premiere doit encore porter "
                    "le compteur de 4 a 5 (preuve que la capacite part bel et bien a ce palier), la seconde doit "
                    "le laisser bloque a 5 (preuve du plafond) -- contrairement a un montage direct a 5, ce cas "
                    "ne peut pas passer si Absorption ne se declenche plus du tout.",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg011')", "Puzzle.Counter('hg011', 'energy', 4)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('01001a')", "Puzzle.Attack('01001a')"],
        "cibles": ["hg011"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["hg011", "energy", 5]], "attributs_carte": [["hg011", "attack", 5]]},
    },
    {
        "nom": "[hg] hg011, second Forced Response : apres QU'ELLE attaque, elle retire 1 compteur energy (3 -> 2, "
               "+3 ATK -> +2 ATK)",
        "pourquoi": "« Forced Response: After she attacks, remove 1 energy counter from this card. » Montage a 3 "
                    "compteurs (`Puzzle.Counter`), puis elle attaque l'identite (`Puzzle.EnemyAttacks`, aucune "
                    "alliee ne defend) : un seul compteur part, pas tous.",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg011')", "Puzzle.Counter('hg011', 'energy', 3)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EnemyAttacks('hg011', '01001a')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["hg011", "energy", 2]], "attributs_carte": [["hg011", "attack", 2]]},
    },
    {
        "nom": "[hg] hg011, TEMOIN A VIDE : sans aucun compteur, elle attaque quand meme (0 ATK bonus) -> le "
               "retrait ne casse rien et reste a 0, pas de compteur negatif",
        "pourquoi": "« remove 1 energy counter » sans minimum imprime : contre-cas de securite, aucune garde "
                    "manuelle n'est codee (RemoveCountersInternal est sans danger a vide) -- ce cas le prouve "
                    "en jeu plutot qu'en lecture de code seule.",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg011')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EnemyAttacks('hg011', '01001a')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["hg011", "energy", 0]], "attributs_carte": [["hg011", "attack", 0]]},
    },

    # ============================================================ hg012 : Zombie Thor
    {
        "nom": "[hg] hg012 Storm : apres que Zombie Thor active CONTRE LE JOUEUR en ATTAQUANT (forme heros), "
               "chaque allie qu'il controle subit 1 degat -- l'identite n'est touchee QUE par l'attaque elle-meme",
        "pourquoi": "« Storm — Forced Response: After Zombie Thor activates against a player, deal 1 damage to "
                    "each ally that player controls. » Forme heros -> Puzzle.Activate declenche une ATTAQUE "
                    "(non defendue, pas de defenseur designe) : l'identite encaisse les 3 ATQ imprimes de Thor, "
                    "ET separement chacune des 2 allies en jeu subit le degat propre de Storm (1 chacune, pas "
                    "partage). 01050 Hulk (5 PV) et 01002 Black Cat (2 PV) survivent toutes les deux a 1 degat.",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg012')",
                          "Puzzle.PutIntoPlay('01050', under_control=True)", "Puzzle.PutIntoPlay('01002', under_control=True)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Activate('hg012')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 3, "degats": [["01050", 1], ["01002", 1]], "en_jeu": ["01050", "01002"]},
    },
    {
        "nom": "[hg] hg012 Storm, TEMOIN « ACTIVATES couvre aussi la MANIGANCE » : forme alter-ego (pas d'attaque "
               "possible), Zombie Thor active quand meme -> l'allie subit quand meme 1 degat",
        "pourquoi": "« ACTIVATES against a player », pas « attacks » : la capacite doit partir aussi quand "
                    "l'activation est une manigance (forme alter-ego). Contre-preuve du mot-piege ACTIVATES "
                    "vs ATTACKS deja documente sur nt013/27158 : un filtre reduit a AfterUnitAttackUnit "
                    "laisserait ce cas a 0 degat.",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('hg012')", "Puzzle.PutIntoPlay('01050', under_control=True)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Activate('hg012')"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01050", 1]]},
    },
    {
        "nom": "[hg] hg012 TEMOIN SANS ALLIE : Zombie Thor active, aucun allie en jeu -> rien a cibler, aucun crash, "
               "degats d'attaque normaux sur l'identite seulement",
        "pourquoi": "contre-cas de securite : `DealDamage` sur une liste vide (joueur sans allie) ne doit rien "
                    "casser et ne doit rien infliger a l'identite -- Storm ne vise jamais « each character »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg012')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Activate('hg012')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 3},
    },

    # ============================================================ hg013 : Zombie Black Widow
    {
        "nom": "[hg] hg013 : une alliee (01002 Black Cat) ne peut pas defendre contre Zombie Black Widow",
        "pourquoi": "« Allies cannot defend against Zombie Black Widow's attacks. » Mesure la legalite `IsCanDefense` que "
                    "le moteur consulte avant d'offrir la defense (modele `ap305`), pas le resultat d'une attaque deja "
                    "resolue (le defenseur impose par le harnais contournerait la question).",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('hg013')", "Puzzle.PutIntoPlay('01002', under_control=True)"],
        "main_exclusive": ["01088"],
        "declencher": [],
        "verifier": "hg_peut_defendre_etat",
        "attendu": {"peut_defendre": [["01002", "hg013", False]]},
    },
    {
        "nom": "[hg] hg013 contre-cas « ZOMBIE BLACK WIDOW's attacks » : la MEME alliee peut defendre contre un AUTRE ennemi (hg007) "
               "pendant que hg013 est en jeu -- l'interdiction ne vise QUE les attaques de hg013",
        "pourquoi": "« against ZOMBIE BLACK WIDOW's attacks », pas « against enemy attacks » (modele ap305, generique) : "
                    "preuve que `who_attacker=\"This\"` mord vraiment, pas un filtre Enemy generique qui bloquerait aussi hg007",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('hg013')", "Puzzle.PutIntoPlay('hg007')",
                          "Puzzle.PutIntoPlay('01002', under_control=True)"],
        "main_exclusive": ["01088"],
        "declencher": [],
        "verifier": "hg_peut_defendre_etat",
        "attendu": {"peut_defendre": [["01002", "hg007", True], ["01002", "hg013", False]]},
    },
    {
        "nom": "[hg] hg013 ligne de base : SANS hg013 en jeu, la meme alliee peut defendre contre hg007",
        "pourquoi": "contre-cas de securite : prouve que l'interdiction ne fuit pas vers un AUTRE Metazombie en l'absence de hg013",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('hg007')", "Puzzle.PutIntoPlay('01002', under_control=True)"],
        "main_exclusive": ["01088"],
        "declencher": [],
        "verifier": "hg_peut_defendre_etat",
        "attendu": {"peut_defendre": [["01002", "hg007", True]]},
    },

    # ============================================================ hg014 : Zombie Doctor Strange
    {
        "nom": "[hg] hg014 Hex : apres que Zombie Doctor Strange active CONTRE LE JOUEUR en ATTAQUANT (forme heros), "
               "l'identite subit l'attaque normale (1 ATQ) ET recoit en plus 1 carte de rencontre face cachee",
        "pourquoi": "« Hex — Forced Response: After Zombie Doctor Strange activates against you, deal yourself 1 "
                    "facedown encounter card. » Pas de clause « instead of » (a la difference de Just a Core, "
                    "hg001-hg003) : l'attaque se resout normalement EN PLUS de la carte distribuee.",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg014')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Activate('hg014')"],
        "passer_sur_option": "Defense",
        "verifier": "hg014_etat",
        "attendu": {"degats_identite": 1, "cartes_distribuees": 1},
    },
    {
        "nom": "[hg] hg014 Hex, TEMOIN « ACTIVATES couvre aussi la MANIGANCE » : forme alter-ego (pas d'attaque "
               "possible), Zombie Doctor Strange active quand meme -> la carte de rencontre est distribuee quand meme",
        "pourquoi": "« ACTIVATES against you », pas « attacks » : la capacite doit partir aussi quand l'activation "
                    "est une manigance (forme alter-ego). Contre-preuve du mot-piege ACTIVATES vs ATTACKS deja "
                    "documente sur hg012/nt013/27158 : un filtre reduit a AfterUnitAttackUnit laisserait ce cas a "
                    "0 carte distribuee.",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('hg014')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Activate('hg014')"],
        "verifier": "hg014_etat",
        "attendu": {"degats_identite": 0, "cartes_distribuees": 1},
    },
    {
        "nom": "[hg] hg014 contre-cas « ZOMBIE DOCTOR STRANGE active » : l'activation d'un AUTRE Metazombie "
               "(hg007) pendant que hg014 est en jeu ne distribue AUCUNE carte -- Hex ne vise que SA PROPRE "
               "activation",
        "pourquoi": "preuve que `AfterEnemyActivatesAgainstYou(..., \"This\", ...)` mord bien sur hg014 "
                    "specifiquement, pas sur « n'importe quel ennemi actif » -- contre-cas de securite comme "
                    "hg013 (« ZOMBIE BLACK WIDOW's attacks », pas « enemy attacks »).",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg014')", "Puzzle.PutIntoPlay('hg007')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Activate('hg007')"],
        "passer_sur_option": "Defense",
        "verifier": "hg014_etat",
        "attendu": {"cartes_distribuees": 0},
    },

    # ============================================================ hg015 : Zombie Magik
    {
        "nom": "[hg] hg015 Portal to Limbo : pas engage avec un sbire -> fouille le deck de rencontre, trouve "
               "le sbire, le met en jeu engage avec le joueur, PUIS remelange la defausse de rencontre",
        "pourquoi": "« After Zombie Magik activates against you, if you are not engaged with any minions, discard "
                    "cards from the encounter deck until a minion is discarded and put it into play engaged with "
                    "you. Then shuffle the encounter discard pile into the encounter deck. » Deck truque "
                    "[01105, 01105, 01110] : le premier 01105 part en boost (sans effet, desc vide), la fouille "
                    "defausse le second 01105 puis trouve 01110 (Minion) -> mis en jeu engage. Le remelange qui "
                    "suit doit remettre les 01105 defausses dans le deck (dans_deck_rencontre), preuve que "
                    "« Then shuffle » part vraiment et pas seulement la fouille.",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('hg015')",
                          "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01110')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Activate('hg015')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["01110"], "dans_deck_rencontre": ["01105"]},
    },
    {
        "nom": "[hg] hg015 TEMOIN « ACTIVATES couvre aussi la MANIGANCE » : forme alter-ego (pas d'attaque "
               "possible), Zombie Magik active quand meme -> le sbire entre en jeu",
        "pourquoi": "« ACTIVATES against you », pas « attacks » : la capacite doit partir aussi quand l'activation "
                    "est une manigance (forme alter-ego). Contre-preuve du mot-piege ACTIVATES vs ATTACKS deja "
                    "documente sur hg012/nt013/27158 : un filtre reduit a AfterUnitAttackUnit laisserait ce cas "
                    "sans aucun sbire en jeu.",
        "scenario": "rhino", "heros": "spider_man",
        # ⚠ Deck a 2 cartes, pas 1 : en forme alter-ego, l'activation de hg015 est une MANIGANCE, qui tire
        # DEJA sa propre carte de boost dans le deck de rencontre avant que la capacite "Portal to Limbo" ne
        # cherche a son tour. Avec un deck a une seule carte, cette carte partait en boost de la manigance et
        # n'atteignait jamais la fouille (ECHEC constate le 27/10/2026, passe de verification groupee : "01110
        # n'est pas en jeu"). 01105 ("I'm Tough", desc vide) absorbe ce premier tirage, 01110 (Minion) reste
        # disponible pour la fouille de hg015.
        "mise_en_place": ["Puzzle.PutIntoPlay('hg015')",
                          "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01110')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Activate('hg015')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["01110"]},
    },
    {
        "nom": "[hg] hg015 contre-cas « engage avec un sbire » : la garde bloque TOUTE la capacite, le sbire visible "
               "au sommet du deck de rencontre reste dans le deck, jamais fouille",
        "pourquoi": "« if you are NOT engaged with any minions » : deja engage (01101 Hydra Mercenary mis en jeu "
                    "avant, auto-engage comme tout Minion.PutIntoPlay) -> rien ne doit se passer, ni fouille ni "
                    "remelange ni spawn de Metazombie. Modele Kingpin (60159b/60160b) : la condition gate "
                    "l'ability ENTIERE, pas seulement sa premiere phrase.",
        "scenario": "rhino", "heros": "spider_man",
        # ⚠ Pas de Minion dans ce deck du tout (contrairement aux cas precedents) : la manigance de hg015 tire
        # de toute facon sa PROPRE carte de boost avant que la garde "pas engage" ne soit evaluee, et l'ordre
        # de tirage d'un deck cree par CreateEncounterDeck n'est pas fiable d'un cas a l'autre (constate le
        # 27/10/2026 : le MEME appel CreateEncounterDeck('01105', '01110') a vu tantot 01105 tire en premier,
        # tantot 01110 -- verifier "01110 reste dans le deck" est donc fragile). La preuve que la garde bloque
        # TOUTE la capacite (pas seulement la fouille) tient deja a elle seule dans l'absence de tout second
        # Minion en jeu : seul 01101, deja en jeu avant l'activation, y reste.
        "mise_en_place": ["Puzzle.PutIntoPlay('01101', under_control=True)", "Puzzle.PutIntoPlay('hg015')",
                          "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Activate('hg015')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["01101"]},
    },

    # ============================================================ hg016 Thrown Shield
    {
        "nom": "[hg] hg016 Thrown Shield : revelee, heros en forme HEROS + 1 allie en jeu -> 2 degats a chacun",
        "pourquoi": "« When Revealed: Deal 2 damage to each hero and each ally in play »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('01050', under_control=True)"],
        "declencher": ["Puzzle.Reveal('hg016')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2, "degats": [["01050", 2]]},
    },
    {
        "nom": "[hg] hg016 Thrown Shield, TEMOIN forme ALTER-EGO : le heros reste en Alter-Ego n'encaisse rien, "
               "l'allie encaisse quand meme 2",
        "pourquoi": "« each HERO » : une identite en forme Alter-Ego n'est pas comptee par Worlds.GetOnFieldHeroes "
                    "-- prouve que le filtre de forme mord vraiment (sans lui, la carte punirait aussi un joueur "
                    "reste prudemment en Alter-Ego)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": ["Puzzle.PutIntoPlay('01050', under_control=True)"],
        "declencher": ["Puzzle.Reveal('hg016')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0, "degats": [["01050", 2]]},
    },
    {
        "nom": "[hg] hg016 Thrown Shield, partie a DEUX heros : les DEUX heros encaissent 2 degats chacun",
        "pourquoi": "« each hero » sans « that player »/« you » : aucun filtre par joueur, contrairement a "
                    "hg012 Zombie Thor (« each ally THAT PLAYER controls »)",
        "scenario": "rhino", "heros": "spider_man", "heros2": "hawkeye",
        "mise_en_place": ["Puzzle.ChangeForm('01001b')", "Puzzle.ChangeForm('04001b')"],
        "declencher": ["Puzzle.Reveal('hg016')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2, "degats": [["04001a", 2]]},
    },
    {
        "nom": "[hg] hg016 Thrown Shield, TEMOIN aucun allie en jeu : seul le heros encaisse, aucun plantage "
               "sur une liste d'allies vide",
        "pourquoi": "« each ally in play » doit tolerer AUCUN allie present (Worlds.GetOnFieldAllies peut "
                    "renvoyer une liste vide) sans lever d'exception",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS],
        "declencher": ["Puzzle.Reveal('hg016')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2},
    },

    # ============================================================ hg017 : Avengers, Feast!
    {
        "nom": "[hg] hg017 contre-cas : AUCUN Metazombie en jeu (seul Rhino, sans trait METAZOMBIE) -> rien ne se declenche, aucun crash",
        "pourquoi": "« Each Metazombie in play » : prouve que le filtre `Metazombies(effect)` exclut bien un Villain SANS le trait "
                    "(Rhino), et que la carte ne plante pas quand la liste est vide",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg017')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0},
    },
    {
        "nom": "[hg] hg017 un seul Metazombie (hg013, ATK 1) en jeu, joueur en forme Heros : il active en ATTAQUE contre le joueur -> 1 degat sur l'identite",
        "pourquoi": "« Each Metazombie in play activates against each player » : un seul Metazombie -> une seule activation, "
                    "egale a son ATK imprime (hg013 : ATK 1, pas d'autre capacite qui modifie sa propre attaque)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg013')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg017')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01001a", 1]]},
    },
    {
        "nom": "[hg] hg017 DEUX Metazombies en jeu (hg009 ATK 4 + hg013 ATK 1) : chacun active -> degats CUMULES (5) sur l'identite du seul joueur",
        "pourquoi": "« EACH Metazombie » : preuve que la carte boucle sur TOUS les Metazombies en jeu, pas seulement celui qui porte "
                    "le jeton actif de la phase mechant normale (aucune regle de jeton posee dans ce montage, scenario rhino)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg009')", "Puzzle.PutIntoPlay('hg013')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg017')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01001a", 5]]},
    },
    {
        "nom": "[hg] hg017 TEMOIN « ACTIVATES couvre aussi la MANIGANCE » : joueur en forme Alter-Ego, hg013 (SCH 1) active en "
               "MANIGANCE contre le complot principal -> menace +1, AUCUN degat sur l'identite",
        "pourquoi": "meme piege que hg012 (« ACTIVATES couvre l'attaque ET la manigance ») : DoActivate doit basculer sur DoSchemes "
                    "quand le joueur vise est en Alter-Ego, pas rester bloque sur une attaque",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.SetThreat('01097b', 0)", "Puzzle.PutIntoPlay('hg013')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg017')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 1]], "degats_identite": 0},
    },
    {
        "nom": "[hg] hg017 A DEUX JOUEURS (spider_man + hawkeye, tous deux en forme Heros), UN Metazombie (hg013, ATK 1) en jeu : "
               "il active CONTRE CHAQUE JOUEUR -> 1 degat sur CHAQUE identite",
        "pourquoi": "« against EACH PLAYER » : preuve que la boucle vise tous les joueurs de la partie, pas seulement le joueur courant "
                    "ou celui qui revele la carte",
        "scenario": "rhino", "heros": "spider_man", "heros2": "hawkeye",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.ChangeForm('04001b')", "Puzzle.PutIntoPlay('hg013')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg017')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01001a", 1], ["04001a", 1]]},
    },
    {
        "nom": "[hg] hg017 « Do not deal boost cards » : deck de rencontre reduit a des Charge (01099, Boost 2 / ATK+3), hg013 (ATK "
               "1) active via la carte -> degats = ATK NU (1), aucune carte piochee (01099 reste dans le deck)",
        "pourquoi": "« Do not deal boost cards for these activations » = `do_not_give_boost=True` ; Charge, s'il etait pioche, "
                    "ajouterait un ATK+3 (modele de la fiche mots-cles/boost.md) -- sa seule presence prouve l'ABSENCE de pioche "
                    "si les degats restent a 1",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('hg013')",
                          "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01099', '01099', '01099')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg017')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01001a", 1]], "dans_deck_rencontre": ["01099"]},
    },
    {
        "nom": "[hg] hg017 TEMOIN du precedent : MEME montage mais activation DIRECTE (Puzzle.Activate, sans do_not_give_boost) -> "
               "le boost EST pioche, degats = 1 (ATK) + 2 (icones Boost de Charge) = 3",
        "pourquoi": "contre-cas de securite : prouve que Charge AURAIT bien ajoute du degat si la suppression de hg017 etait absente -- "
                    "sans ce temoin, le cas precedent pourrait passer au vert simplement parce que Charge n'ajoute jamais rien",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('hg013')",
                          "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01099', '01099', '01099')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Activate('hg013')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01001a", 3]]},
    },

    # ============================================================ hg006 : Inside Galactus
    {
        "nom": "[hg] hg006 Residual Cosmic Power : +1 ATK sur le mechant ACTIF (Rhino, jeton par defaut)",
        "pourquoi": "« The villain gets +1 ATK. » Rhino (01094, ATQ imprimee 2) porte le jeton actif par defaut.",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg006')"],
        "main_exclusive": ["01088"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["01094", "attack", 1]]},
    },
    {
        "nom": "[hg] hg006 +1 ATK suit le jeton actif : passe sur hg001 des qu'il devient le mechant actif",
        "pourquoi": "« The villain » = celui qui porte le jeton, dynamique : contre-cas qui prouve que le bonus n'est pas fige sur Rhino",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg006')", "Puzzle.PutIntoPlay('hg001')",
                          "Puzzle.SetActiveVillain('hg001')"],
        "main_exclusive": ["01088"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["01094", "attack", 0]]},
    },
    {
        "nom": "[hg] hg006 Digestive Juices : 2 degats indirects a chaque joueur en fin de phase du mechant",
        "pourquoi": "« Forced Response: At the end of the villain phase, deal 2 indirect damage to each player. »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg006')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EndVillainPhase()"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2},
    },

    # ============================================================ hg004a/hg004b : mise en place du scenario reel
    {
        "nom": "[hg] hg004a Setup (ms_marvel, aucune exclusion) : Coeur hg001 en jeu, 2 Metazombies, Horde deck au complet (9)",
        "pourquoi": "Ms. Marvel n'a ni Metazombie ni Fallen Heroes homonyme (contrairement a Spider-Man, qui EST hg010) : aucune exclusion attendue",
        "scenario": "the_hunger_core", "heros": "ms_marvel",
        "mise_en_place": [],
        "declencher": [],
        "verifier": "hg_setup_etat",
        "attendu": {"villain_en_jeu": "hg001", "n_metazombies": 2, "horde_total": 9, "horde_absent": None},
    },
    {
        "nom": "[hg] hg004a Setup (iron_man) : la version zombie d'Iron Man (hg008) n'est JAMAIS dans le Horde deck",
        "pourquoi": "« Set aside the zombie version of each chosen hero » : Iron Man choisi -> hg008 exclu du Horde deck (8 au lieu de 9)",
        "scenario": "the_hunger_core", "heros": "iron_man",
        "mise_en_place": [],
        "declencher": [],
        "verifier": "hg_setup_etat",
        "attendu": {"villain_en_jeu": "hg001", "n_metazombies": 2, "horde_total": 8, "horde_absent": "hg008"},
    },
    {
        "nom": "[hg] hg004a Setup (wolverine) : son allie Survivor (hg076) et son Trapped Survivor (hg055) sont retires du jeu",
        "pourquoi": "« If someone plays one of those heroes (for example, Wolverine), remove that ally and its Trapped Survivor from the game »",
        "scenario": "the_hunger_core", "heros": "wolverine",
        "mise_en_place": [],
        "declencher": [],
        "verifier": "hg_setup_etat",
        "attendu": {"retires": ["hg076", "hg055"]},
    },

    # ============================================================ hg004b : Deeper Inside (Forced Interrupt + perte sur manigance accomplie)
    # ⚠ hg004a (face A, AUCUNE menace imprimee) auto-avance vers hg004b des la mise en place : c'est le moteur generique
    # (`MainScheme.OnAfterCardRevealedEnd`, « printed_target_threat == None » -> `self.Advance(None, effect)`), pas du code
    # a nous. hg004b (menace 9, bien imprimee) EST donc deja en jeu apres un simple `"mise_en_place": []`. Meme regle pour
    # hg005a (AUCUNE menace imprimee non plus) : des que l'avancee l'atteint elle se retourne IMMEDIATEMENT en hg005b, qui
    # a sa propre menace (11) et s'y arrete. D'ou l'etat final « hg005b » directement, aussi bien ici que pour les cas hg005b.
    {
        "nom": "[hg] hg004b Deeper Inside : le Coeur qui serait vaincu avance plutot vers hg002, ET la manigance passe au stade 2 (hg005b, via hg005a sans menace)",
        "pourquoi": "« Forced Interrupt: When The Hunger Core would be defeated, instead advance to stage 2 of the main scheme "
                    "and put the next stage of The Hunger Core into play. »",
        "scenario": "the_hunger_core", "heros": "ms_marvel",
        "mise_en_place": [],
        "declencher": ["Puzzle.Damage('hg001', 999)"],
        "verifier": "hg_manigance_etat",
        "attendu": {"complot": "hg005b", "mechant": "hg002", "fin": None},
    },
    {
        "nom": "[hg] hg004b accompli (9[per_hero] menaces, solo) : les joueurs PERDENT",
        "pourquoi": "« If this scheme is completed, the players lose. »",
        "scenario": "the_hunger_core", "heros": "ms_marvel",
        "mise_en_place": [],
        "declencher": ["Puzzle.SetThreat('hg004b', 9)"],
        "verifier": "hg_manigance_etat",
        "attendu": {"fin": "perdu"},
    },

    # ============================================================ hg005b : The Innards (When Revealed + perte sur manigance accomplie)
    {
        "nom": "[hg] hg005b revelee (1 pas d'avancee depuis la manigance deja en jeu, via hg005a sans menace) : Inside Galactus entre en jeu, "
               "le Horde deck fournit 2 Metazombies supplementaires MAIS le plafond (max. 3) bloque le 3e",
        "pourquoi": "« When Revealed: Put \"Inside Galactus\" and 2 Metazombies into play (max. 3 in play). » "
                    "La mise en place (hg004a) a deja mis 2 Metazombies en jeu : le 1er des deux nouveaux porte a 3 (plafond atteint), le 2nd est refuse.",
        "scenario": "the_hunger_core", "heros": "ms_marvel",
        "mise_en_place": ["Puzzle.AdvanceMainScheme()"],
        "declencher": [],
        "verifier": "hg_manigance_etat",
        "attendu": {"complot": "hg005b", "n_metazombies": 3, "environnement_en_jeu": "Inside Galactus"},
    },
    {
        "nom": "[hg] hg005b accompli (11[per_hero] menaces, solo) : les joueurs PERDENT",
        "pourquoi": "« If this scheme is completed, the players lose. »",
        "scenario": "the_hunger_core", "heros": "ms_marvel",
        "mise_en_place": ["Puzzle.AdvanceMainScheme()"],
        "declencher": ["Puzzle.SetThreat('hg005b', 11)"],
        "verifier": "hg_manigance_etat",
        "attendu": {"fin": "perdu"},
    },

    # ============================================================ hg018 : Dented Vibranium Shield
    {
        "nom": "[hg] hg018 Dented Vibranium Shield : posee avec Zombie Captain America en jeu -> s'attache a lui et lui donne Retaliate 2",
        "pourquoi": "« Attach to Zombie Captain America. Zombie Captain America gains Retaliate 2 » : AttachToFaceWhenPutIntoPlay + "
                    "GiveKeywordToAttached, verifie par le mot-cle lu sur la carte hote une fois attachee",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": ["Puzzle.PutIntoPlay('hg007')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.PutIntoPlay('hg018')"],
        "verifier": "etat_attendu",
        "attendu": {"accroche_a": [["hg018", "hg007"]], "attributs_carte": [["hg007", "retaliate", 2]]},
    },
    {
        "nom": "[hg] hg018 TEMOIN : Zombie Captain America SANS le bouclier n'a aucune Riposte",
        "pourquoi": "contre-cas de securite : prouve que Retaliate 2 vient bien de l'attachement, pas d'une valeur imprimee sur hg007",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": ["Puzzle.PutIntoPlay('hg007')"],
        "main_exclusive": ["01088"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["hg007", "retaliate", 0]]},
    },
    {
        "nom": "[hg] hg018 Retaliate 2 EN JEU : le heros attaque Zombie Captain America equipe du bouclier -> 2 degats en retour sur son identite",
        "pourquoi": "preuve bout-en-bout que le mot-cle donne par GiveKeywordToAttached est bien lu par le moteur au moment de "
                    "l'attaque (fiche retaliate.md)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('hg007')", "Puzzle.PutIntoPlay('hg018')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('01001a')"],
        "cibles": ["hg007"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2},
    },
    {
        "nom": "[hg] hg018 CONTRE-CAS : posee SANS Zombie Captain America en jeu -> aucune cible d'attache, defaussee, aucun plantage",
        "pourquoi": "AttachToFaceWhenPutIntoPlay sans cible legale ne doit pas faire planter la pose ; le moteur defausse "
                    "l'attachement faute d'hote (meme comportement que le temoin hg026). Attendu initial « reste en jeu » "
                    "corrige le 27/10/2026 : un attachement sans hote ne reste pas en jeu",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.PutIntoPlay('hg018')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["hg018"]},
    },
    {
        "nom": "[hg] hg018 Hero Action : depenser 2 ressources (n'importe quel type) -> le bouclier est defausse et Zombie Captain America reperd Retaliate",
        "pourquoi": "« Hero Action: Spend 2 resources -> discard this card » ; la perte de Retaliate confirme que GiveKeywordToAttached "
                    "ne vaut QUE tant que la carte est attachee",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('hg007')", "Puzzle.PutIntoPlay('hg018')"],
        "main_exclusive": ["01089", "01090"],
        "declencher": ["Puzzle.Action('hg018', 'HeroAction')"],
        "payer_avec": ["01089", "01090"],
        "payer_tout": True,
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["hg018"], "attributs_carte": [["hg007", "retaliate", 0]]},
    },

    # ============================================================ hg019 : Necrotic Repulsors
    # ⚠ Tous les cas hg019-hg023 commencent par `IRON_MAN_NU` : l'entree en jeu de hg008 attache une amelioration
    # TIREE AU HASARD de son deck signature (hg019-hg022), ce qui rendait chaque cas (et surtout chaque TEMOIN)
    # dependant du melange (ex. temoin hg019 : 1 chance sur 4 que hg019 soit deja la, Piercing actif).
    {
        "nom": "[hg] hg019 Necrotic Repulsors : attache a Zombie Iron Man (ATK 1 + 1 amelioration = 2), son attaque PERCE un heros "
               "Tenace -> 2 degats ET la carte Tenace est defaussee",
        "pourquoi": "« His attacks gain Piercing » : modele `27078` Venom 'Now We're Angry!' "
                    "(UnitAttackGainKeyword(CardFinder(name=...), piercing=True)) -- la carte Tenace doit etre "
                    "defaussee ET les degats doivent passer (contrairement a une Tenace qui bloque simplement)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg008')", IRON_MAN_NU,
                          "Puzzle.AttachReel('hg019', 'hg008')", "Puzzle.Tough('01001a')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EnemyAttacks('hg008', '01001a')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2, "statuts_absents": [["01001a", "Tough"]]},
    },
    {
        "nom": "[hg] hg019 TEMOIN (sans Necrotic Repulsors attache) : la MEME attaque de Zombie Iron Man contre "
               "un heros Tenace est BLOQUEE (0 degat), la carte Tenace est quand meme defaussee",
        "pourquoi": "contre-cas de substitution : prouve que c'est bien hg019 qui fait passer les degats au cas "
                    "precedent, pas une autre capacite de hg008",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg008')", IRON_MAN_NU, "Puzzle.Tough('01001a')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EnemyAttacks('hg008', '01001a')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0, "statuts_absents": [["01001a", "Tough"]]},
    },
    {
        "nom": "[hg] hg019 Hero Action : depenser 2 ressources (n'importe quel type) -> Necrotic Repulsors "
               "defaussee de Zombie Iron Man",
        "pourquoi": "« Hero Action: Spend 2 resources -> discard this card » : modele `sq017` Revealed Identity "
                    "(meme texte officiel), PlayerActionToDiscardThis + SetCost(Cost(\"2\"))",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('hg008')", IRON_MAN_NU, "Puzzle.AttachReel('hg019', 'hg008')"],
        "main_exclusive": ["01088", "01089"],
        "declencher": ["Puzzle.Action('hg019', 'HeroAction')"],
        "payer_avec": ["01088", "01089"],
        "verifier": "etat_attendu",
        "attendu": {"defausse_rencontre": ["hg019"]},
    },

    # ============================================================ hg020 : Patched Armor
    {
        "nom": "[hg] hg020 Patched Armor : attachee a Zombie Iron Man, +2* PV (scale par nombre de heros)",
        "pourquoi": "« Zombie Iron Man gets +2* hit points » : GiveKeywordToAttached(health=\"2*\"), scale comme le PV de base "
                    "(solo : +2). `attributs_carte` mesure l'ECART de PV max a l'imprime (cle `health` -> max_health).",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": ["Puzzle.PutIntoPlay('hg008')", IRON_MAN_NU],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.AttachReel('hg020', 'hg008')"],
        "verifier": "etat_attendu",
        "attendu": {"accroche_a": [["hg020", "hg008"]], "attributs_carte": [["hg008", "health", 2]]},
    },
    {
        "nom": "[hg] hg020 Hero Action : depenser 3 ressources -> defaussee, le bonus de PV disparait",
        "pourquoi": "« Hero Action: Spend 3 resources -> discard this card » ; GiveKeywordToAttached retire le bonus a la sortie de jeu",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('hg008')", IRON_MAN_NU, "Puzzle.AttachReel('hg020', 'hg008')"],
        "main_exclusive": ["01088", "01089"],
        "declencher": ["Puzzle.Action('hg020', 'HeroAction')"],
        "payer_avec": ["01088", "01089"],
        "payer_tout": True,
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["hg020"], "attributs_carte": [["hg008", "health", 0]]},
    },

    # ============================================================ hg021 : Rotten Thrusters
    {
        "nom": "[hg] hg021 Rotten Thrusters : attachee a Zombie Iron Man, +1 SCH",
        "pourquoi": "« Zombie Iron Man gets +1 SCH » : GiveKeywordToAttached(Villain, scheme=1), mesure par "
                    "attributs_carte (un ECART de +1 SCH, pas une valeur absolue)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": ["Puzzle.PutIntoPlay('hg008')", IRON_MAN_NU],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.AttachReel('hg021', 'hg008')"],
        "verifier": "etat_attendu",
        "attendu": {"accroche_a": [["hg021", "hg008"]], "attributs_carte": [["hg008", "scheme", 1]]},
    },
    {
        "nom": "[hg] hg021 cannot be attacked by allies : une alliee (Black Cat 01002) ne peut pas attaquer "
               "Zombie Iron Man attache de Rotten Thrusters (0 degat)",
        "pourquoi": "« cannot be attacked by allies » : UnitCannotBeAttacked('AttachedVillain', "
                    "conditions=[Ally.IsType(attacker)]). ⚠ PAS Hulk 01050 : sa Forced Response apres attaque (defausse "
                    "du dessus du deck -> 2 degats a un ennemi) blessait hg008 PAR CAPACITE, pas par attaque (faux echec "
                    "du 27/10/2026, 2 degats mesures)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('hg008')", IRON_MAN_NU,
                          "Puzzle.AttachReel('hg021', 'hg008')", "Puzzle.PutIntoPlay('01002', under_control=True)"],
        "declencher": ["Puzzle.Attack('01002')"],
        "cibles": ["hg008"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["hg008", 0]]},
    },
    {
        "nom": "[hg] hg021 TEMOIN du precedent : sans Rotten Thrusters, la meme alliee (Black Cat) attaque bien "
               "Zombie Iron Man",
        "pourquoi": "ligne de base : sans ce temoin, le cas precedent pourrait passer au vert simplement parce "
                    "qu'aucun allie ne peut jamais attaquer un Villain par defaut",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('hg008')", IRON_MAN_NU,
                          "Puzzle.PutIntoPlay('01002', under_control=True)"],
        "declencher": ["Puzzle.Attack('01002')"],
        "cibles": ["hg008"],
        "verifier": "etat_attendu",
        "attendu": {"degats_min": [["hg008", 1]]},
    },
    {
        "nom": "[hg] hg021 Hero Action : depenser 2 ressources (any type) -> defausser Rotten Thrusters",
        "pourquoi": "PlayerActionToDiscardThis(HeroAction).SetCost(Cost(\"2\")) (cout generique au lieu de colore)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('hg008')", IRON_MAN_NU, "Puzzle.AttachReel('hg021', 'hg008')"],
        "declencher": ["Puzzle.Action('hg021', 'HeroAction')"],
        "main_exclusive": ["01090"],
        "payer_avec": ["01090"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["hg021"]},
    },

    # ============================================================ hg022 : Necrotic Unibeam
    {
        "nom": "[hg] hg022 Necrotic Unibeam, Overkill : hg008 (ATK1 +1 par attache = ATK2) attaque l'identite, "
               "01002 Black Cat (2 PV, deja a 1 degat donc 1 PV restant) defend -> elle meurt, 1 degat d'exces "
               "a l'identite (Overkill, ennemi abat un allie -> l'exces va au controleur)",
        "pourquoi": "« His attacks gain Overkill » + mots-cles/overkill.md",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg008')", IRON_MAN_NU,
                          "Puzzle.PutIntoPlay('01002', under_control=True)",
                          "Puzzle.Damage('01002', 1)", "Puzzle.AttachReel('hg022', 'hg008')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EnemyAttacks('hg008', '01001b', defender='01002')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["01002"], "degats_identite": 1},
    },
    {
        "nom": "[hg] hg022 TEMOIN (preuve par substitution) : MEME montage mais SANS hg022 attachee -> hg008 reste a "
               "ATK1 (0 attache), 1 PV restant pile suffisant, AUCUN exces (pas d'Overkill)",
        "pourquoi": "contre-cas de securite",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg008')", IRON_MAN_NU,
                          "Puzzle.PutIntoPlay('01002', under_control=True)", "Puzzle.Damage('01002', 1)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EnemyAttacks('hg008', '01001b', defender='01002')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["01002"], "degats_identite": 0},
    },
    {
        "nom": "[hg] hg022 Necrotic Unibeam, degat aux allies : hg008 (ATK2 avec hg022 attachee) attaque l'identite "
               "SANS defenseur -> l'identite encaisse 2 ATQ, ET chacune des 2 alliees en jeu subit SEPAREMENT 1 degat",
        "pourquoi": "« deal 1 damage to each ally controlled by the attacked player »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg008')", IRON_MAN_NU,
                          "Puzzle.PutIntoPlay('01050', under_control=True)",
                          "Puzzle.PutIntoPlay('01002', under_control=True)", "Puzzle.AttachReel('hg022', 'hg008')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EnemyAttacks('hg008', '01001b')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2, "degats": [["01050", 1], ["01002", 1]], "en_jeu": ["01050", "01002"]},
    },
    {
        "nom": "[hg] hg022 TEMOIN (preuve par substitution) : MEME montage mais SANS hg022 attachee -> hg008 reste "
               "ATK1, l'identite encaisse 1, AUCUN degat aux allies",
        "pourquoi": "contre-cas de securite",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg008')", IRON_MAN_NU,
                          "Puzzle.PutIntoPlay('01050', under_control=True)",
                          "Puzzle.PutIntoPlay('01002', under_control=True)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EnemyAttacks('hg008', '01001b')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 1, "degats": [["01050", 0], ["01002", 0]], "en_jeu": ["01050", "01002"]},
    },
    {
        "nom": "[hg] hg022 Hero Action : depenser [mental][mental][mental] (2 cartes Genius) -> hg022 defaussee, "
               "hg008 retombe a 0 attache (et ATK 1)",
        "pourquoi": "« Hero Action: Spend 3 [mental] resources -> discard this card. »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg008')", IRON_MAN_NU,
                          "Puzzle.AttachReel('hg022', 'hg008')"],
        "main_exclusive": ["01089", "01089"],
        "declencher": ["Puzzle.Action('hg022', 'HeroAction')"],
        "payer_avec": ["01089", "01089"],
        "verifier": "etat_attendu",
        "attendu": {"defausse_rencontre": ["hg022"], "taille_attaches": [["hg008", 0]], "attributs_carte": [["hg008", "attack", 0]]},
    },
    {
        "nom": "[hg] hg022 Hero Action REFUSEE : une seule carte Genius (2 [mental] < 3) -> hg022 reste attachee",
        "pourquoi": "contre-cas du cout colore « 3 [mental] » : deux ressources ne suffisent pas (declencher_tolerant : "
                    "l'echec de la commande EST le resultat attendu)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg008')", IRON_MAN_NU,
                          "Puzzle.AttachReel('hg022', 'hg008')"],
        "main_exclusive": ["01089"],
        "declencher": [],
        "declencher_tolerant": ["Puzzle.Action('hg022', 'HeroAction')"],
        "verifier": "etat_attendu",
        "attendu": {"accroche_a": [["hg022", "hg008"]], "taille_attaches": [["hg008", 1]]},
    },

    # ============================================================ hg023 : Hunger Protocol
    {
        "nom": "[hg] hg023 Hunger Protocol : Zombie Iron Man porte 2 ameliorations (hg020 + hg021, ATK 1+2 = 3) -> il "
               "ACTIVE contre le joueur en forme heros -> 3 degats, aucune amelioration de plus",
        "pourquoi": "« If Zombie Iron Man has 2 or more attachments, he activates against you. » (DoActivate, attaque "
                    "reelle -> passer_sur_option Defense). hg020/hg021 choisies car sans effet sur l'attaque.",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg008')", IRON_MAN_NU,
                          "Puzzle.AttachReel('hg020', 'hg008')", "Puzzle.AttachReel('hg021', 'hg008')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg023')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 3, "taille_attaches": [["hg008", 2]]},
    },
    {
        "nom": "[hg] hg023 Hunger Protocol : Zombie Iron Man n'a qu'UNE amelioration (celle de son entree en jeu) -> PAS "
               "d'activation, une 2e amelioration est tiree de son deck signature et attachee",
        "pourquoi": "« Otherwise, discard cards from his signature deck until an attachment is discarded and attach it to "
                    "him; then shuffle » : meme fouille partagee que hg008 (DefausserJusquaUneAmeliorationDuDeckSignature). "
                    "Aucun degat : la branche « activates » ne doit pas partir aussi.",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg008')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg023')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0, "taille_attaches": [["hg008", 2]]},
    },
    {
        "nom": "[hg] hg023 Hunger Protocol « If you cannot » : Zombie Iron Man absent -> la carte gagne Surge, la carte "
               "semee au sommet (01126) est revelee",
        "pourquoi": "« If you cannot, this card gains Surge. » ; deck truque [01105, 01126] (01126 au sommet), modele hc015",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01126')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg023')"],
        "accepter_choix": True,
        "verifier": "etat_attendu",
        "attendu": {"carte_du_surge": "01126", "dans_deck_rencontre": ["01105"]},
    },

    # ============================================================ hg024 : Hulk Hungry!
    {
        "nom": "[hg] hg024 Hulk Hungry! : joueur en ALTER-EGO -> il passe en forme heros, puis Zombie Hulk (ATK 4) l'attaque -> 4 degats",
        "pourquoi": "« When Revealed: If you are in alter-ego form, change to hero form. Zombie Hulk activates against you. » "
                    "Pas de FORME_HEROS : le joueur demarre en alter-ego ; l'activation doit etre une ATTAQUE (forme heros) "
                    "et non une manigance, preuve que le changement de forme precede l'activation",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('hg009')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg024')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"forme": "Hero", "degats_identite": 4},
    },
    {
        "nom": "[hg] hg024 TEMOIN : joueur DEJA en forme heros -> pas de changement de forme, Zombie Hulk active quand meme -> 4 degats",
        "pourquoi": "la seconde phrase (« Zombie Hulk activates against you ») n'est pas conditionnee a la premiere",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg009')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg024')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"forme": "Hero", "degats_identite": 4},
    },
    {
        "nom": "[hg] hg024 CONTRE-CAS : Zombie Hulk absent -> le joueur passe en forme heros, aucune activation, aucun plantage",
        "pourquoi": "Worlds.FindVillain(name='Zombie Hulk') rend None : la carte doit seulement changer la forme",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg024')"],
        "verifier": "etat_attendu",
        "attendu": {"forme": "Hero", "degats_identite": 0},
    },

    # ============================================================ hg025 : Smash
    {
        "nom": "[hg] hg025 Smash : choix Support, DEUX supports controles -> les DEUX sont defausses, aucun degat a l'identite",
        "pourquoi": "« Choose support or upgrade and discard EACH card of that type you control »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS,
                          "Puzzle.PutIntoPlay('01026', under_control=True)", "Puzzle.PutIntoPlay('01034', under_control=True)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg025')"],
        "choisir_option": "Support",
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0, "hors_jeu": ["01026", "01034"]},
    },
    {
        "nom": "[hg] hg025 Smash contre-cas « THAT type » : choix Support alors qu'un Upgrade (01018) est controle mais AUCUN support -> "
               "l'Upgrade n'est PAS touche, le heros subit 3 degats",
        "pourquoi": "« discard each card of THAT type » : le type NON choisi reste intact",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('01018', under_control=True)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg025')"],
        "choisir_option": "Support",
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 3, "en_jeu": ["01018"]},
    },
    {
        "nom": "[hg] hg025 Smash : choix Upgrade, DEUX upgrades controles -> les deux defausses, aucun degat",
        "pourquoi": "Symetrique du cas Support",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS,
                          "Puzzle.PutIntoPlay('01018', under_control=True)", "Puzzle.PutIntoPlay('01008', under_control=True)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg025')"],
        "choisir_option": "Upgrade",
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0, "hors_jeu": ["01018", "01008"]},
    },
    {
        "nom": "[hg] hg025 Smash : choix Upgrade, AUCUN upgrade controle -> le heros subit 3 degats",
        "pourquoi": "« If you control none, your hero takes 3 damage » cote Upgrade aussi",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg025')"],
        "choisir_option": "Upgrade",
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 3},
    },

    # ============================================================ hg026 : Endless Rage
    {
        "nom": "[hg] hg026 Endless Rage : attachee a Zombie Hulk, qui gagne STEADY et +1 ATK (4 -> 5)",
        "pourquoi": "« Attach to Zombie Hulk. Zombie Hulk gains Steady and gets +1 ATK »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg009')"],
        "declencher": ["Puzzle.Reveal('hg026')"],
        "verifier": "etat_attendu",
        "attendu": {
            "en_jeu": ["hg026"],
            "accroche_a": [["hg026", "hg009"]],
            "attributs_carte": [["hg009", "attack", 1], ["hg009", "steady", 1]],
        },
    },
    {
        "nom": "[hg] hg026 TEMOIN : Zombie Hulk absent de la table -> la carte ne peut pas s'attacher, "
               "defaussee automatiquement, aucun plantage",
        "pourquoi": "preuve que le CardFinder ne trouve rien a vide",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS],
        "declencher": ["Puzzle.Reveal('hg026')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["hg026"]},
    },
    {
        "nom": "[hg] hg026 Hero Action : depenser 3 ressources (n'importe quel type) defausse la carte",
        "pourquoi": "« Hero Action: Spend 3 resources -> discard this card » (2 cartes de base = 4 ressources >= 3)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg009')", "Puzzle.PutIntoPlay('hg026')"],
        "main_exclusive": ["01088", "01089"],
        "declencher": ["Puzzle.Action('hg026', 'HeroAction')"],
        "payer_avec": ["01088", "01089"],
        "payer_tout": True,
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["hg026"], "attributs_carte": [["hg009", "attack", 0], ["hg009", "steady", 0]]},
    },

    # ============================================================ hg027 : Rotten Web
    {
        "nom": "[hg] hg027 Rotten Web : attache au heros -> -1 ATK et -1 THW, DEF inchangee",
        "pourquoi": "« Attach to your hero. Your hero gets -1 ATK and -1 THW. »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('hg027')"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["01001a", "attack", -1], ["01001a", "thwart", -1], ["01001a", "defense", 0]]},
    },
    {
        "nom": "[hg] hg027 Hero Action : 3 ressources de TYPES DIFFERENTS (Energy+Genius+Strength) -> hg027 defaussee, malus disparait",
        "pourquoi": "« Hero Action (any player): Spend 3 resources of different types -> discard this card. »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('hg027')"],
        "declencher": ["Puzzle.Action('hg027', 'HeroAction')"],
        "main_exclusive": ["01088", "01089", "01090"],
        "payer_tout": True,
        "payer_avec": ["01088", "01089", "01090"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["hg027"], "attributs_carte": [["01001a", "attack", 0], ["01001a", "thwart", 0]]},
    },
]

# ================================================================================================================
# hg028-hg076 : fusion du 27/10/2026 (49 cartes scriptees par des agents separes, cas ecrits ici a partir du texte
# imprime et du code). Memes conventions que plus haut : `RIEN_A_BOOSTER` des qu'une activation peut piocher un
# boost, `"passer_sur_option": "Defense"` sur toute attaque REELLE contre l'identite sans defenseur impose.
# Verificateur dedie `hg_etat_plus` (en fin de fichier) pour ce que `etat_attendu` ne sait pas lire (cartes
# retirees du jeu, taille d'un deck signature, Metazombie a demi-PV, nombre de cartes Tenace) ; il delegue le reste
# a `etat_attendu`.
CAS += [
    # ============================================================ hg028 : Dead Spider-Sense
    {
        "nom": "[hg] hg028 Dead Spider-Sense (solo) : Zombie Spider-Man active contre le seul joueur, en forme heros -> 2 degats ET etourdi (Web)",
        "pourquoi": "« Zombie Spider-Man activates against the player with the most cards in hand » : seul joueur -> lui",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg010')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg028')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2, "statuts": [["01001a", "Stunned"]]},
    },
    {
        "nom": "[hg] hg028 CONTRE-CAS : Zombie Spider-Man absent -> rien ne se passe, aucun plantage",
        "pourquoi": "garde `FindCardOnField(...) is None` : aucune activation fantome",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg028')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0},
    },
    {
        "nom": "[hg] hg028 A DEUX JOUEURS : Hawkeye a la plus grosse main (3 cartes contre 1) -> c'est LUI qui est attaque, pas le joueur qui revele",
        "pourquoi": "« the player with THE MOST cards in hand » : la cible n'est pas « you » quand un autre joueur a strictement plus de cartes",
        "scenario": "rhino", "heros": "spider_man", "heros2": "hawkeye",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.ChangeForm('04001b')", "Puzzle.PutIntoPlay('hg010')",
                          "Puzzle.EmptyHand(siege=1)", "Puzzle.CreateHandCards('01088', '01089', '01090', siege=1)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg028')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0, "degats": [["04001a", 2]]},
    },
    {
        "nom": "[hg] hg028 A DEUX JOUEURS, EGALITE (1 carte chacun) -> « If tied, he activates against YOU » : le joueur qui revele est attaque",
        "pourquoi": "« If tied, he activates against you »",
        "scenario": "rhino", "heros": "spider_man", "heros2": "hawkeye",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.ChangeForm('04001b')", "Puzzle.PutIntoPlay('hg010')",
                          "Puzzle.EmptyHand(siege=1)", "Puzzle.CreateHandCards('01089', siege=1)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg028')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2, "degats": [["04001a", 0]]},
    },

    # ============================================================ hg029 : Rooftop to Rooftop
    {
        "nom": "[hg] hg029 Rooftop to Rooftop en jeu : Zombie Spider-Man gagne +1 SCH",
        "pourquoi": "« While this scheme is in play, Zombie Spider-Man gets +1 SCH »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('hg010')", "Puzzle.PutIntoPlay('hg029')"],
        "main_exclusive": ["01088"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["hg029"], "attributs_carte": [["hg010", "scheme", 1]]},
    },
    {
        "nom": "[hg] hg029 « cannot be attacked by allies » : Black Cat (01002) ne blesse pas Zombie Spider-Man",
        "pourquoi": "meme fabrique que hg021 (UnitCannotBeAttacked + filtre Ally sur l'attaquant)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg010')", "Puzzle.PutIntoPlay('hg029')",
                          "Puzzle.PutIntoPlay('01002', under_control=True)"],
        "declencher": ["Puzzle.Attack('01002')"],
        "cibles": ["hg010"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["hg010", 0]]},
    },
    {
        "nom": "[hg] hg029 TEMOIN « by ALLIES » : le HEROS, lui, attaque Zombie Spider-Man normalement (2 degats)",
        "pourquoi": "le filtre ne vise que les allies : un heros n'est pas bloque",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg010')", "Puzzle.PutIntoPlay('hg029')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('01001a')"],
        "cibles": ["hg010"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["hg010", 2]]},
    },

    # ============================================================ hg030 : Rotten Binary
    {
        "nom": "[hg] hg030 Rotten Binary : heros en forme HEROS + 1 allie -> 1 degat a chacun",
        "pourquoi": "« Deal 1 damage to each hero and each ally in play »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('01050', under_control=True)"],
        "declencher": ["Puzzle.Reveal('hg030')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 1, "degats": [["01050", 1]]},
    },
    {
        "nom": "[hg] hg030 TEMOIN forme ALTER-EGO : l'identite n'encaisse rien (pas un « hero »), l'allie encaisse quand meme 1",
        "pourquoi": "« each HERO » : Worlds.GetOnFieldHeroes ignore une identite en alter-ego",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": ["Puzzle.PutIntoPlay('01050', under_control=True)"],
        "declencher": ["Puzzle.Reveal('hg030')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0, "degats": [["01050", 1]]},
    },

    # ============================================================ hg031 : Photon Fist
    {
        "nom": "[hg] hg031 Photon Fist revelee avec Zombie Captain Marvel en jeu -> s'attache a elle",
        "pourquoi": "« Attach to Zombie Captain Marvel » (AttachToFaceWhenPutIntoPlay, voie generique Reveal -> PutIntoPlay)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('hg011')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg031')"],
        "verifier": "etat_attendu",
        "attendu": {"accroche_a": [["hg031", "hg011"]]},
    },
    {
        "nom": "[hg] hg031 Overkill : Zombie Captain Marvel (ATK 1 + 2 energy = 3) abat Black Cat (2 PV) qui defend -> 1 degat d'exces a l'identite",
        "pourquoi": "« Her attacks gain Overkill » + mots-cles/overkill.md (ennemi abat un allie -> exces au controleur)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg011')", "Puzzle.Counter('hg011', 'energy', 2)",
                          "Puzzle.Reveal('hg031')", "Puzzle.PutIntoPlay('01002', under_control=True)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EnemyAttacks('hg011', '01001b', defender='01002')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["01002"], "degats_identite": 1},
    },
    {
        "nom": "[hg] hg031 TEMOIN (preuve par substitution) : MEME montage SANS Photon Fist -> Black Cat meurt, AUCUN exces",
        "pourquoi": "contre-cas : l'Overkill vient bien de hg031, pas de Zombie Captain Marvel elle-meme",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg011')", "Puzzle.Counter('hg011', 'energy', 2)",
                          "Puzzle.PutIntoPlay('01002', under_control=True)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EnemyAttacks('hg011', '01001b', defender='01002')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["01002"], "degats_identite": 0},
    },
    {
        "nom": "[hg] hg031 Hero Action : depenser 2 ressources (n'importe quel type) -> Photon Fist defaussee",
        "pourquoi": "« Hero Action: Spend 2 resources -> discard this card »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg011')", "Puzzle.Reveal('hg031')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Action('hg031', 'HeroAction')"],
        "payer_avec": ["01088"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["hg031"]},
    },

    # ============================================================ hg032 : Discharge
    {
        "nom": "[hg] hg032 Discharge : 2 energy -> +1 (3), puis tout retire, elle est etourdie, 3 degats indirects au joueur",
        "pourquoi": "« If ... fewer than 5 energy counters, place 1 on her. Then remove all ...; she is stunned. Deal indirect damage "
                    "equal to the removed counters to each player. »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg011')", "Puzzle.Counter('hg011', 'energy', 2)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg032')"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["hg011", "energy", 0]], "statuts": [["hg011", "Stunned"]], "degats_identite": 3},
    },
    {
        "nom": "[hg] hg032 Discharge DEJA A 5 : pas de compteur ajoute (« fewer than 5 »), 5 retires -> 5 degats indirects",
        "pourquoi": "la pose est conditionnelle, le retrait ne l'est pas",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg011')", "Puzzle.Counter('hg011', 'energy', 5)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg032')"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["hg011", "energy", 0]], "degats_identite": 5},
    },
    {
        "nom": "[hg] hg032 CONTRE-CAS : Zombie Captain Marvel absente -> aucun effet, aucun plantage",
        "pourquoi": "garde defensive (sujet absent)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg032')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0},
    },

    # ============================================================ hg033 : Energy Hunger
    {
        "nom": "[hg] hg033 Energy Hunger : 2 compteurs energy sur Zombie Captain Marvel -> +2 ATK",
        "pourquoi": "« Place 2 energy counters on Zombie Captain Marvel (max. 5) » + Absorption (+1 ATK par compteur)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('hg011')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg033')"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["hg011", "energy", 2]], "attributs_carte": [["hg011", "attack", 2]]},
    },
    {
        "nom": "[hg] hg033 Energy Hunger, PLAFOND : deja a 4 -> 5 (max. 5), pas 6",
        "pourquoi": "« (max. 5) »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('hg011')", "Puzzle.Counter('hg011', 'energy', 4)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg033')"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["hg011", "energy", 5]], "attributs_carte": [["hg011", "attack", 5]]},
    },

    # ============================================================ hg034 : Bloodied Mjolnir
    {
        "nom": "[hg] hg034 Bloodied Mjolnir revele avec Zombie Thor -> attache, +1 ATK",
        "pourquoi": "« Attach to Zombie Thor. Zombie Thor gets +1 ATK. »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('hg012')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg034')"],
        "verifier": "etat_attendu",
        "attendu": {"accroche_a": [["hg034", "hg012"]], "attributs_carte": [["hg012", "attack", 1]]},
    },
    {
        "nom": "[hg] hg034 Storm +1 : Zombie Thor (ATK 3+1) active contre le heros -> 4 degats a l'identite, l'allie subit 1 (Storm) + 1 (Mjolnir) = 2",
        "pourquoi": "« Storm deals 1 additional damage to each ally » (s'ajoute au degat de hg012)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg012')", "Puzzle.Reveal('hg034')",
                          "Puzzle.PutIntoPlay('01050', under_control=True)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Activate('hg012')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 4, "degats": [["01050", 2]]},
    },
    {
        "nom": "[hg] hg034 Piercing : l'attaque de Zombie Thor perce un heros Tenace -> 4 degats ET la Tenace est defaussee",
        "pourquoi": "« His attacks gain Overkill and Piercing »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg012')", "Puzzle.Reveal('hg034')",
                          "Puzzle.Tough('01001a')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EnemyAttacks('hg012', '01001a')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 4, "statuts_absents": [["01001a", "Tough"]]},
    },
    {
        "nom": "[hg] hg034 Hero Action : depenser 3 ressources -> Mjolnir defausse, Zombie Thor reperd son +1 ATK",
        "pourquoi": "« Hero Action: Spend 3 resources -> discard this card »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg012')", "Puzzle.Reveal('hg034')"],
        "main_exclusive": ["01088", "01089"],
        "declencher": ["Puzzle.Action('hg034', 'HeroAction')"],
        "payer_avec": ["01088", "01089"],
        "payer_tout": True,
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["hg034"], "attributs_carte": [["hg012", "attack", 0]]},
    },

    # ============================================================ hg035 : Rotten Lightning
    {
        "nom": "[hg] hg035 Rotten Lightning : heros + allie -> 2 degats a chacun",
        "pourquoi": "« Deal 2 damage to each friendly character »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('01050', under_control=True)"],
        "declencher": ["Puzzle.Reveal('hg035')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2, "degats": [["01050", 2]]},
    },
    {
        "nom": "[hg] hg035 « friendly CHARACTER » couvre l'ALTER-EGO : l'identite encaisse 2 meme en alter-ego",
        "pourquoi": "contraste avec hg030 (« each HERO ») : un personnage ami inclut l'identite quelle que soit sa forme",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('hg035')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2},
    },

    # ============================================================ hg036 : Fallen God of Thunder
    {
        "nom": "[hg] hg036 Fallen God of Thunder : Zombie Thor blesse (5) soigne 4 -> 1 degat restant, PAS d'activation",
        "pourquoi": "« Zombie Thor heals 4* damage. If he had no damage, he activates against you. » (solo : 4*)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg012')", "Puzzle.Damage('hg012', 5)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg036')"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["hg012", 1]], "degats_identite": 0},
    },
    {
        "nom": "[hg] hg036 Zombie Thor INDEMNE -> il active contre le joueur (forme heros : attaque de 3)",
        "pourquoi": "« If he had no damage, he activates against you »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg012')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg036')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"degats": [["hg012", 0]], "degats_identite": 3},
    },

    # ============================================================ hg037 : Widow's Bite
    {
        "nom": "[hg] hg037 Widow's Bite (ALTER-EGO) : 1 compteur infection ET la carte gagne Surge (01126 seme au sommet est revele)",
        "pourquoi": "« When Revealed (Alter-Ego): Place 1 infection counter. This card gains Surge. »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01126')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg037')"],
        "accepter_choix": True,
        "verifier": "etat_attendu",
        "attendu": {"compteurs_identite": [["infection", 1]], "carte_du_surge": "01126"},
    },
    {
        "nom": "[hg] hg037 Widow's Bite (HEROS) : le heros est etourdi ET 1 compteur infection, pas de Surge",
        "pourquoi": "« When Revealed (Hero): Your hero is stunned. Place 1 infection counter. »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01126')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg037')"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs_identite": [["infection", 1]], "statuts": [["01001a", "Stunned"]],
                    "dans_deck_rencontre": ["01126"]},
    },

    # ============================================================ hg038 : Infiltrator
    {
        "nom": "[hg] hg038 Infiltrator en jeu : Zombie Black Widow gagne +1 SCH",
        "pourquoi": "« While this scheme is in play, Zombie Black Widow gets +1 SCH »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('hg013')", "Puzzle.PutIntoPlay('hg038')"],
        "main_exclusive": ["01088"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["hg038"], "attributs_carte": [["hg013", "scheme", 1]]},
    },

    # ============================================================ hg039 : Sleeper Agent
    {
        "nom": "[hg] hg039 Sleeper Agent : joueur en ALTER-EGO -> passe en heros, Zombie Black Widow l'attaque (1 degat)",
        "pourquoi": "« If you are in alter-ego form, change to hero form. Zombie Black Widow activates against you. »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('hg013')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg039')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"forme": "Hero", "degats_identite": 1},
    },
    {
        "nom": "[hg] hg039 CONTRE-CAS : Zombie Black Widow absente -> passage en heros seulement, aucun plantage",
        "pourquoi": "garde `if villain:`",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg039')"],
        "verifier": "etat_attendu",
        "attendu": {"forme": "Hero", "degats_identite": 0},
    },

    # ============================================================ hg040 : Rotten Eye of Agamotto
    {
        "nom": "[hg] hg040 Rotten Eye : attache a Zombie Doctor Strange, 3 degats -> 2",
        "pourquoi": "« Each time Zombie Doctor Strange would take damage, reduce that damage by 1 »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('hg014')", "Puzzle.Reveal('hg040')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Damage('hg014', 3)"],
        "verifier": "etat_attendu",
        "attendu": {"accroche_a": [["hg040", "hg014"]], "degats": [["hg014", 2]]},
    },
    {
        "nom": "[hg] hg040 « EACH time » : deux coups de 3 -> 2 + 2 = 4 (pas limite a la premiere fois, contrairement a hg007)",
        "pourquoi": "« Each time » : aucune limite par phase",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('hg014')", "Puzzle.Reveal('hg040')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Damage('hg014', 3)", "Puzzle.Damage('hg014', 3)"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["hg014", 4]]},
    },
    {
        "nom": "[hg] hg040 Hero Action : depenser [mental][mental] (Genius) -> defaussee",
        "pourquoi": "« Hero Action: Spend 2 [mental] resources -> discard this card »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg014')", "Puzzle.Reveal('hg040')"],
        "main_exclusive": ["01089"],
        "declencher": ["Puzzle.Action('hg040', 'HeroAction')"],
        "payer_avec": ["01089"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["hg040"]},
    },

    # ============================================================ hg041 : Crimson Bands of Cyttorak
    {
        "nom": "[hg] hg041 Crimson Bands : attachee au heros, qui ne peut plus attaquer (Rhino reste a 0 degat)",
        "pourquoi": "« Attach to your hero. Your hero cannot attack. »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.Reveal('hg041')"],
        "main_exclusive": ["01088"],
        "declencher": [],
        "declencher_tolerant": ["Puzzle.Attack('01001a')"],
        "verifier": "etat_attendu",
        "attendu": {"accroche_a": [["hg041", "01001a"]], "degats": [["01094", 0]]},
    },
    {
        "nom": "[hg] hg041 Hero Action : 2 ressources de TYPES DIFFERENTS + incliner le heros -> defaussee, heros incline",
        "pourquoi": "« Spend 2 resources of different types and exhaust your hero -> discard this card »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.Reveal('hg041')"],
        "main_exclusive": ["01088", "01090"],
        "declencher": ["Puzzle.Action('hg041', 'HeroAction')"],
        "payer_avec": ["01088", "01090"],
        "payer_tout": True,
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["hg041"], "exhausted": ["01001a"]},
    },

    # ============================================================ hg042 : Hunger Hex
    {
        "nom": "[hg] hg042 Hunger Hex en jeu : taille de main du joueur -2",
        "pourquoi": "« While this scheme is in play, each player's hand size is reduced by 2 »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg042')"],
        "main_exclusive": ["01088"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["hg042"], "attributs_carte": [["01001a", "hand_size", -2]]},
    },

    # ============================================================ hg043 : Soulsword
    {
        "nom": "[hg] hg043 Soulsword revelee avec Zombie Magik -> attachee, +1 ATK",
        "pourquoi": "« Attach to Zombie Magik. Zombie Magik gets +1 ATK. » (AttachToFaceWhenPutIntoPlay ajoute a la fusion)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('hg015')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg043')"],
        "verifier": "etat_attendu",
        "attendu": {"accroche_a": [["hg043", "hg015"]], "attributs_carte": [["hg015", "attack", 1]]},
    },
    {
        "nom": "[hg] hg043 Piercing : Zombie Magik (ATK 2+1) perce un heros Tenace -> 3 degats, Tenace defaussee",
        "pourquoi": "« Her attacks gain Piercing »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg015')", "Puzzle.Reveal('hg043')",
                          "Puzzle.Tough('01001a')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EnemyAttacks('hg015', '01001a')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 3, "statuts_absents": [["01001a", "Tough"]]},
    },
    {
        "nom": "[hg] hg043 Hero Action : depenser 3 ressources -> Soulsword defaussee, Zombie Magik reperd +1 ATK",
        "pourquoi": "« Hero Action: Spend 3 resources -> discard this card »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg015')", "Puzzle.Reveal('hg043')"],
        "main_exclusive": ["01088", "01089"],
        "declencher": ["Puzzle.Action('hg043', 'HeroAction')"],
        "payer_avec": ["01088", "01089"],
        "payer_tout": True,
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["hg043"], "attributs_carte": [["hg015", "attack", 0]]},
    },

    # ============================================================ hg044 : Teleportation Disc
    {
        "nom": "[hg] hg044 Teleportation Disc : Zombie Magik active contre le joueur SANS boost (deck de Charge 01099) -> 2 degats nus",
        "pourquoi": "« Zombie Magik activates against each player. Do not deal boost cards for these activations. » "
                    "Charge (Boost 2) pioche aurait ajoute 2 : 2 degats prouvent l'absence de pioche.",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('hg015')",
                          "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01099', '01099', '01099')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg044')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2},
    },
    {
        "nom": "[hg] hg044 A DEUX JOUEURS : Zombie Magik active contre CHAQUE joueur -> 2 degats sur chaque identite",
        "pourquoi": "« against EACH player »",
        "scenario": "rhino", "heros": "spider_man", "heros2": "hawkeye",
        "mise_en_place": [FORME_HEROS, "Puzzle.ChangeForm('04001b')", "Puzzle.PutIntoPlay('hg015')",
                          "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01099', '01099', '01099')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg044')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01001a", 2], ["04001a", 2]]},
    },

    # ============================================================ hg045 : Demons of Limbo
    {
        "nom": "[hg] hg045 Demons of Limbo : le sbire de la defausse de rencontre qui a le PLUS de PV (01101, 3 PV) entre en jeu, 01110 (2 PV) reste",
        "pourquoi": "« Put the minion with the most hit points in the encounter discard pile into play engaged with you »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.EmptyEncounterDiscardPile()", "Puzzle.CreateEncounterDiscardPile('01110', '01101')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg045')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["01101"], "defausse_rencontre": ["01110"]},
    },

    # ============================================================ hg046 : Metazombie Power!
    {
        "nom": "[hg] hg046 Metazombie Power! : Zombie Spider-Man seul Metazombie en jeu -> le dessus de SON deck signature est revele (3 -> 2 cartes)",
        "pourquoi": "« Reveal the top card of the active Metazombie's signature deck » (jeton sur Rhino -> repli sur le premier Metazombie, "
                    "`LeMetazombieActif`). La carte revelee est tiree au hasard : seul le COMPTE du deck est deterministe.",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('hg010')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg046')"],
        "verifier": "hg_etat_plus",
        "attendu": {"deck_signature": [["hg010", 2]]},
    },
    {
        "nom": "[hg] hg046 AUCUN Metazombie en jeu -> la carte gagne Surge (01126 seme au sommet est revele)",
        "pourquoi": "« If there are no Metazombies in play, this card gains Surge. »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01126')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg046')"],
        "accepter_choix": True,
        "verifier": "etat_attendu",
        "attendu": {"carte_du_surge": "01126"},
    },

    # ============================================================ hg047 : Rise of the Horde!
    {
        "nom": "[hg] hg047 Rise of the Horde! (scenario reel, 2 Metazombies apres la mise en place) -> un 3e entre en jeu depuis le Horde deck",
        "pourquoi": "« If there are fewer than 3 Metazombies in play, put one into play. »",
        "scenario": "the_hunger_core", "heros": "ms_marvel",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('hg047')"],
        "verifier": "hg_manigance_etat",
        "attendu": {"n_metazombies": 3},
    },
    {
        "nom": "[hg] hg047 DEJA 3 Metazombies -> aucun 4e, la carte gagne Surge (01126 revele)",
        "pourquoi": "« Otherwise, this card gains Surge. »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": ["Puzzle.PutIntoPlay('hg007')", "Puzzle.PutIntoPlay('hg013')", "Puzzle.PutIntoPlay('hg014')",
                          "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01126')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg047')"],
        "accepter_choix": True,
        "verifier": "etat_attendu",
        "attendu": {"carte_du_surge": "01126"},
    },

    # ============================================================ hg048 : Half-Eaten
    {
        "nom": "[hg] hg048 Half-Eaten (scenario reel) : un 3e Metazombie entre en jeu avec des degats = moitie de ses PV (arrondi bas)",
        "pourquoi": "« put one into play with damage equal to half its hit points » ; degats POSES (SetHealth), pas infliges : "
                    "le Shield de hg007 ne doit pas les reduire, quel que soit le Metazombie tire",
        "scenario": "the_hunger_core", "heros": "ms_marvel",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('hg048')"],
        "verifier": "hg_etat_plus",
        "attendu": {"n_metazombies": 3, "metazombie_demi_pv": True},
    },
    {
        "nom": "[hg] hg048 DEJA 3 Metazombies -> la carte gagne Surge (01126 revele)",
        "pourquoi": "« Otherwise, this card gains Surge. »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": ["Puzzle.PutIntoPlay('hg007')", "Puzzle.PutIntoPlay('hg013')", "Puzzle.PutIntoPlay('hg014')",
                          "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01126')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg048')"],
        "accepter_choix": True,
        "verifier": "etat_attendu",
        "attendu": {"carte_du_surge": "01126"},
    },

    # ============================================================ hg049 : Hunger Pulse
    {
        "nom": "[hg] hg049 Hunger Pulse, Coeur EXPOSE (aucun Metazombie) -> 2[per_hero] menace sur le complot principal",
        "pourquoi": "« Place 1* threat on the main scheme (2* if the Core is exposed) » ; expose = aucun Metazombie (symetrie hg001)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.SetThreat('01097b', 0)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg049')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 2]]},
    },
    {
        "nom": "[hg] hg049 Hunger Pulse, Coeur BLINDE (hg007 en jeu) -> 1[per_hero] menace seulement",
        "pourquoi": "valeur de base quand le Coeur n'est pas expose",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.SetThreat('01097b', 0)", "Puzzle.PutIntoPlay('hg007')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg049')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 1]]},
    },
    {
        "nom": "[hg] hg049 [star] Boost : piochee en boost de l'attaque de Rhino -> 1 compteur infection",
        "pourquoi": "« [star] Boost: Place 1 infection counter. »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Boost('hg049')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"compteurs_identite": [["infection", 1]]},
    },

    # ============================================================ hg050 : The Hive Calls
    {
        "nom": "[hg] hg050 The Hive Calls (aucun texte) : revelee, entre en jeu avec sa menace de depart 4[per_hero], aucun plantage",
        "pourquoi": "manigance annexe sans texte (precedent 01156/16054) : tout est natif (StartingThreat, Acceleration, Boost)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg050')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["hg050"], "menace": [["hg050", 4]]},
    },

    # ============================================================ hg051-hg055 : Trapped Survivor
    {
        "nom": "[hg] hg051 Trapped Survivor : apres l'etape 1 de la phase du mechant, 1 compteur et 2[per_hero] menace ici",
        "pourquoi": "« Forced Response: After step 1 of the villain phase, place 1 counter and 2* threat here. » "
                    "Alter-ego : Rhino manigance (pas de question de defense).",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('hg051')", "Puzzle.SetThreat('hg051', 4)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.RunVillainPhase()"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["hg051", "counter", 1]], "menace": [["hg051", 6]]},
    },
    {
        "nom": "[hg] hg051 A 3 COMPTEURS : la manigance ET Franklin Richards (mis de cote) sont retires du jeu, 1 infection par joueur",
        "pourquoi": "« At 3 counters, remove this card and Franklin Richards from the game; each player places 1 infection counter. »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('hg051')", "Puzzle.Counter('hg051', 'counter', 2)",
                          "Puzzle.MoveTo('hg072', 'AsideScenario')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.RunVillainPhase()"],
        "verifier": "hg_etat_plus",
        "attendu": {"retires": ["hg051", "hg072"], "compteurs_identite": [["infection", 1]]},
    },
    {
        "nom": "[hg] hg051 TEMOIN du seuil : a 1 compteur (-> 2), la manigance reste en jeu, aucune infection",
        "pourquoi": "« AT 3 counters » : rien avant le seuil",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('hg051')", "Puzzle.Counter('hg051', 'counter', 1)",
                          "Puzzle.MoveTo('hg072', 'AsideScenario')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.RunVillainPhase()"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["hg051"], "compteurs": [["hg051", "counter", 2]], "compteurs_identite": [["infection", 0]]},
    },
]

# When Defeated : meme texte sur les 5 manigances, seul l'allie change -> un cas par carte (preuve que chaque
# fichier pointe le BON allie).
for _sch, _allie, _nom in (("hg051", "hg072", "Franklin Richards"), ("hg052", "hg073", "Chewie"),
                           ("hg053", "hg074", "Valeria Richards"), ("hg054", "hg075", "Blade"),
                           ("hg055", "hg076", "Wolverine")):
    CAS.append({
        "nom": f"[hg] {_sch} When Defeated : derniere menace retiree -> la manigance quitte le jeu, {_nom} ({_allie}) rejoint la main du joueur",
        "pourquoi": f"« When Defeated: Remove this card from the game. The player who defeated it adds {_nom} to their hand from the Survivor deck. »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, f"Puzzle.PutIntoPlay('{_sch}')", f"Puzzle.MoveTo('{_allie}', 'AsideScenario')"],
        "main_exclusive": ["01088"],
        "declencher": [f"Puzzle.SetThreat('{_sch}', 0)"],
        "verifier": "hg_etat_plus",
        "attendu": {"retires": [_sch], "en_main": [_allie]},
    })

CAS += [
    # ============================================================ hg056 : Hungry Zombie (aucun script : Guard natif)
    {
        "nom": "[hg] hg056 Hungry Zombie (Guard natif, aucun script) : engage, il bloque l'attaque du heros contre Rhino",
        "pourquoi": "« Guard. » lu dans `desc` ; fichier .py vide garde (convention du pack, cf. hg050/hg059/hg069/hg076)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.Reveal('hg056')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('01001a')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 0], ["hg056", 2]]},
    },

    # ============================================================ hg057 : Bloated Zombie
    {
        "nom": "[hg] hg057 Bloated Zombie vaincu -> chaque joueur pose 1 compteur infection",
        "pourquoi": "« Forced Response: After this minion is defeated, each player places 1 infection counter. »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('hg057')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Damage('hg057', 99)"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["hg057"], "compteurs_identite": [["infection", 1]]},
    },

    # ============================================================ hg058 : Bite
    {
        "nom": "[hg] hg058 Bite : heros INDEMNE -> 1 compteur infection",
        "pourquoi": "« Place 1 infection counter »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg058')"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs_identite": [["infection", 1]]},
    },
    {
        "nom": "[hg] hg058 Bite : heros BLESSE -> 2 compteurs (remplacement, pas 1 + 2)",
        "pourquoi": "« (2 if your hero has damage on it) » lu comme une valeur de remplacement",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.Damage('01001a', 1)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg058')"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs_identite": [["infection", 2]]},
    },
    {
        "nom": "[hg] hg058 Bite en ALTER-EGO : 1 compteur, aucun plantage sur « your hero »",
        "pourquoi": "garde de securite : le joueur n'a pas de heros en jeu a cet instant",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg058')"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs_identite": [["infection", 1]]},
    },
    {
        "nom": "[hg] hg058 Bite en ALTER-EGO, identite BLESSEE -> 2 compteurs (les degats vivent sur la carte d'identite)",
        "pourquoi": "« your hero has damage on it » : les degats sont partages par les deux faces de l'identite",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.Damage('01001b', 1)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg058')"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs_identite": [["infection", 2]], "degats_identite": 1},
    },

    # ============================================================ hg059 / hg069 : Toughness natif
    {
        "nom": "[hg] hg059 Zombie Luke Cage (Toughness natif) : revele, entre en jeu Tenace",
        "pourquoi": "« Guard. Toughness. » lus dans `desc`, aucun script",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg059')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["hg059"], "statuts": [["hg059", "Tough"]]},
    },
    {
        "nom": "[hg] hg069 Zombie Colossus (Toughness natif) : revele, entre en jeu Tenace",
        "pourquoi": "« Guard. Toughness. » lus dans `desc`, aucun script",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg069')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["hg069"], "statuts": [["hg069", "Tough"]]},
    },

    # ============================================================ hg060 : Zombie Hawkeye
    {
        "nom": "[hg] hg060 Zombie Hawkeye : revele -> 2 degats a chaque allie du joueur",
        "pourquoi": "« When Revealed: Deal 2 damage to each ally you control. »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('01050', under_control=True)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg060')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["hg060"], "degats": [["01050", 2]], "degats_identite": 0},
    },

    # ============================================================ hg061 : Zombie Giant-Man
    {
        "nom": "[hg] hg061 Zombie Giant-Man Overkill : ATK 3 contre Black Cat (2 PV) qui defend -> 1 degat d'exces a l'identite",
        "pourquoi": "« Guard. Overkill. »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg061')", "Puzzle.PutIntoPlay('01002', under_control=True)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EnemyAttacks('hg061', '01001b', defender='01002')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["01002"], "degats_identite": 1},
    },
    {
        "nom": "[hg] hg061 TEMOIN (substitution) : Zombie Hawkeye (hg060, ATK 2, sans Overkill) abat Black Cat -> AUCUN exces",
        "pourquoi": "contre-cas : sans Overkill, l'exces est perdu",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg060')", "Puzzle.PutIntoPlay('01002', under_control=True)",
                          "Puzzle.Damage('01002', 1)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EnemyAttacks('hg060', '01001b', defender='01002')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["01002"], "degats_identite": 0},
    },

    # ============================================================ hg062 / hg063 : Quickstrike (cle desc ajoutee a la fusion)
    {
        "nom": "[hg] hg062 Zombie Wasp Quickstrike : revelee contre un heros, elle l'attaque aussitot (1 degat)",
        "pourquoi": "« Quickstrike. » : `\"Quickstrike\": \"1\"` ajoute au desc de cards_custom.json (le texte l'imprime)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg062')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["hg062"], "degats_identite": 1},
    },
    {
        "nom": "[hg] hg062 Retaliate 2 natif : le heros attaque Zombie Wasp -> 2 degats en retour",
        "pourquoi": "« Retaliate 2. » lu dans `desc`",
        "scenario": "rhino", "heros": "spider_man",
        # hg062 pose AVANT le passage en heros : en forme heros, son Quickstrike l'aurait fait attaquer a l'entree en jeu,
        # le heros (auto-defense du pilote) se serait incline, et son attaque n'aurait jamais eu lieu.
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('hg062')", FORME_HEROS],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('01001a')"],
        "cibles": ["hg062"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2},
    },
    {
        "nom": "[hg] hg063 Zombie Nova Prime Quickstrike : revelee contre un heros, attaque aussitot (2 degats, boost Villainous sans icone)",
        "pourquoi": "« Quickstrike. Villainous. » (deck de rencontre sans icone de boost)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg063')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["hg063"], "degats_identite": 2},
    },

    # ============================================================ hg064 : Zombie Mister Fantastic
    {
        "nom": "[hg] hg064 Zombie Mister Fantastic : revele le dessus du deck signature du Metazombie le PLUS BLESSE (Captain Marvel, 5 PV restants < 9)",
        "pourquoi": "« Reveal the top card of the signature deck of the Metazombie with the fewest remaining hit points. » "
                    "Deck de Zombie Captain Marvel : 6 cartes -> 5 ; celui de Zombie Spider-Man n'est jamais consulte.",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('hg010')", "Puzzle.PutIntoPlay('hg011')", "Puzzle.Damage('hg011', 5)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg064')"],
        "verifier": "hg_etat_plus",
        "attendu": {"deck_signature": [["hg011", 5], ["hg010", None]], "en_jeu": ["hg064"]},
    },

    # ============================================================ hg065 : Zombie Invisible Woman
    {
        "nom": "[hg] hg065 Zombie Invisible Woman : revelee -> l'identite ET chaque allie du joueur sont desorientes",
        "pourquoi": "« When Revealed: Your identity and each ally you control are confused. »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('01050', under_control=True)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg065')"],
        "verifier": "etat_attendu",
        "attendu": {"statuts": [["01001a", "Confused"], ["01050", "Confused"]]},
    },
    {
        "nom": "[hg] hg065 « cannot be dealt damage by attacks from ALLIES » : Black Cat attaque -> 0 degat",
        "pourquoi": "WhenUnitWouldTakeDamage(is_from_attack=True, who_deal_damage=Ally) -> PreventDamage",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg065')", "Puzzle.PutIntoPlay('01002', under_control=True)"],
        "declencher": ["Puzzle.Attack('01002')"],
        "cibles": ["hg065"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["hg065", 0]]},
    },
    {
        "nom": "[hg] hg065 TEMOIN : l'attaque du HEROS la blesse normalement (2 degats)",
        "pourquoi": "seuls les allies sont vises",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg065')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('01001a')"],
        "cibles": ["hg065"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["hg065", 2]]},
    },

    # ============================================================ hg066 : Zombie Thing
    {
        "nom": "[hg] hg066 Zombie Thing : revele -> DEUX cartes Tenace en meme temps",
        "pourquoi": "« This minion gets 2 tough status cards. It can have 2 tough status cards at the same time. »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg066')"],
        "verifier": "hg_etat_plus",
        "attendu": {"tenaces": [["hg066", 2]]},
    },
    {
        "nom": "[hg] hg066 les deux Tenaces absorbent DEUX coups (0 degat), le 3e passe",
        "pourquoi": "preuve en jeu des deux cartes d'etat",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.Reveal('hg066')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Damage('hg066', 3)", "Puzzle.Damage('hg066', 3)", "Puzzle.Damage('hg066', 3)"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["hg066", 3]]},
    },

    # ============================================================ hg067 : Zombie Human Torch
    {
        "nom": "[hg] hg067 Zombie Human Torch : son attaque blesse le heros -> 1 degat a chaque allie du joueur attaque",
        "pourquoi": "« After this minion deals damage with an attack, deal 1 damage to each ally controlled by the attacked player. »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg067')", "Puzzle.PutIntoPlay('01050', under_control=True)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EnemyAttacks('hg067', '01001a')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2, "degats": [["01050", 1]]},
    },
    {
        "nom": "[hg] hg067 TEMOIN « deals damage » : attaque absorbee par une Tenace (0 degat) -> l'allie n'encaisse rien",
        "pourquoi": "sans degats infliges par l'attaque, la reponse ne part pas",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg067')", "Puzzle.PutIntoPlay('01050', under_control=True)",
                          "Puzzle.Tough('01001a')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EnemyAttacks('hg067', '01001a')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0, "degats": [["01050", 0]]},
    },

    # ============================================================ hg068 : Zombie Rhino
    {
        "nom": "[hg] hg068 Zombie Rhino Piercing : ATK 3 contre un heros Tenace -> 3 degats, Tenace defaussee",
        "pourquoi": "« This minion's attacks have Piercing. » (« Charge. » = nom d'ambiance, sans effet)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg068')", "Puzzle.Tough('01001a')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EnemyAttacks('hg068', '01001a')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 3, "statuts_absents": [["01001a", "Tough"]]},
    },

    # ============================================================ hg070 : Zombie Falcon
    {
        "nom": "[hg] hg070 Zombie Falcon : revele -> l'identite est inclinee ET etourdie",
        "pourquoi": "« When Revealed: Exhaust your identity; it is stunned. »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg070')"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["01001a"], "statuts": [["01001a", "Stunned"]]},
    },
    {
        "nom": "[hg] hg070 « cannot be attacked by allies » : Black Cat ne blesse pas Zombie Falcon",
        "pourquoi": "UnitCannotAttackTarget(Ally, cannot_attack=\"This\")",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg070')", "Puzzle.PutIntoPlay('01002', under_control=True)"],
        "declencher": [],
        "declencher_tolerant": ["Puzzle.Attack('01002')"],
        "cibles": ["hg070"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["hg070", 0]]},
    },

    # ============================================================ hg071 : Zombie Quicksilver
    {
        "nom": "[hg] hg071 Super Speed : Zombie Quicksilver active DEUX fois (forme heros, aucun allie) -> 2 + 2 = 4 degats",
        "pourquoi": "« This minion activates twice. »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg071')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Activate('hg071')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 4},
    },
    {
        "nom": "[hg] hg071 avec un allie (01050 Hulk, 5 PV) : ses attaques visent l'ALLIE au lieu de l'identite -> 4 degats sur Hulk, 0 sur l'identite",
        "pourquoi": "« While the engaged player controls an ally, its attacks target one of those allies instead of their identity. »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg071')", "Puzzle.PutIntoPlay('01050', under_control=True)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Activate('hg071')"],
        "verifier": "etat_attendu",
        "passer_sur_option": "Defense",
        "attendu": {"degats_identite": 0, "degats": [["01050", 4]]},
    },

    # ============================================================ hg072 : Franklin Richards
    {
        "nom": "[hg] hg072 Franklin Richards, option 1 : incline -> retire 2 compteurs infection du heros (3 -> 1)",
        "pourquoi": "« Action: Exhaust Franklin Richards -> choose one: Remove 2 infection counters from a hero. »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg072', under_control=True)",
                          "Puzzle.Counter('01001a', 'infection', 3)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Action('hg072', 'Action')"],
        "choisir_option": "Remove_2_infection_counters_from_a_hero",
        "cibles": ["01001a"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs_identite": [["infection", 1]], "exhausted": ["hg072"]},
    },
    {
        "nom": "[hg] hg072 Franklin Richards, option 2 : soigne 2 degats d'un personnage ami (heros blesse de 3 -> 1)",
        "pourquoi": "« Heal 2 damage from a friendly character. »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg072', under_control=True)",
                          "Puzzle.Damage('01001a', 3)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Action('hg072', 'Action')"],
        "choisir_option": "Heal_2_damage_from_a_friendly_character",
        "cibles": ["01001a"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 1, "exhausted": ["hg072"]},
    },

    # ============================================================ hg073 : Chewie
    {
        "nom": "[hg] hg073 Chewie : defausse un sbire ZOMBIE (hg056), Chewie subit 1 degat",
        "pourquoi": "« Action: Exhaust Chewie -> discard a Zombie or Metazombie minion. Chewie takes 1 damage. »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg073', under_control=True)", "Puzzle.PutIntoPlay('hg056')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Action('hg073', 'Action')"],
        "cibles": ["hg056"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["hg056"], "degats": [["hg073", 1]], "exhausted": ["hg073"]},
    },
    {
        "nom": "[hg] hg073 Chewie : defausse un sbire METAZOMBIE (hg059, Fallen Heroes) -> la clause « or Metazombie » mord",
        "pourquoi": "les Fallen Heroes sont des MINIONS au trait METAZOMBIE : lecture stricte « minion » retenue",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg073', under_control=True)", "Puzzle.PutIntoPlay('hg059')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Action('hg073', 'Action')"],
        "cibles": ["hg059"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["hg059"], "degats": [["hg073", 1]]},
    },
    {
        "nom": "[hg] hg073 CONTRE-CAS « MINION » : un Metazombie VILAIN (hg013) n'est pas ciblable -> action indisponible, hg013 reste, Chewie indemne",
        "pourquoi": "« discard a Zombie or Metazombie MINION » : les Metazombies du Horde deck sont des vilains, pas des sbires",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg073', under_control=True)", "Puzzle.PutIntoPlay('hg013')"],
        "main_exclusive": ["01088"],
        "declencher": [],
        "declencher_tolerant": ["Puzzle.Action('hg073', 'Action')"],
        "cibles": ["hg013"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["hg013"], "degats": [["hg073", 0]]},
    },

    # ============================================================ hg074 : Valeria Richards
    {
        "nom": "[hg] hg074 Valeria Richards, option 1 : changer de forme (alter-ego -> heros)",
        "pourquoi": "« Action: Exhaust Valeria Richards -> choose one: Change form. »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('hg074', under_control=True)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Action('hg074', 'Action')"],
        "choisir_option": "Change_form",
        "verifier": "etat_attendu",
        "attendu": {"forme": "Hero", "exhausted": ["hg074"]},
    },
    {
        "nom": "[hg] hg074 Valeria Richards, option 2 : 3[per_hero] degats au Coeur EXPOSE (aucun Metazombie)",
        "pourquoi": "« Deal 3* damage to The Hunger Core. »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('hg001')", "Puzzle.PutIntoPlay('hg074', under_control=True)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Action('hg074', 'Action')"],
        "choisir_option": "Deal_3_damage_per_hero_to_The_Hunger_Core",
        "verifier": "etat_attendu",
        "attendu": {"degats": [["hg001", 3]]},
    },
    {
        "nom": "[hg] hg074 option 2 contre un Coeur BLINDE (hg007 en jeu) -> 0 degat (Shielded by the Horde)",
        "pourquoi": "« cannot be dealt damage » tant qu'un Metazombie est en jeu (hg001)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('hg001')", "Puzzle.PutIntoPlay('hg007')",
                          "Puzzle.PutIntoPlay('hg074', under_control=True)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Action('hg074', 'Action')"],
        "choisir_option": "Deal_3_damage_per_hero_to_The_Hunger_Core",
        "verifier": "etat_attendu",
        "attendu": {"degats": [["hg001", 0]]},
    },

    # ============================================================ hg075 : Blade
    {
        "nom": "[hg] hg075 Blade contre un sbire ZOMBIE (hg056, 3 PV) : ATK 2+2 = 4, le vainc, AUCUN degat consecutif",
        "pourquoi": "« While Blade attacks a Zombie or Metazombie enemy, he gets +2 ATK. If he defeats it, Blade takes no consequential damage. »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg075', under_control=True)", "Puzzle.PutIntoPlay('hg056')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('hg075')"],
        "cibles": ["hg056"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["hg056"], "degats": [["hg075", 0]]},
    },
    {
        "nom": "[hg] hg075 TEMOIN : Blade contre un sbire ordinaire (01101, 3 PV) -> ATK 2 nu, 2 degats, 1 degat consecutif (ATK 2*)",
        "pourquoi": "le bonus et l'immunite ne valent que contre un ZOMBIE/METAZOMBIE",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg075', under_control=True)", "Puzzle.PutIntoPlay('01101')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('hg075')"],
        "cibles": ["01101"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01101", 2], ["hg075", 1]]},
    },

    # ============================================================ hg076 : Wolverine (aucun texte)
    {
        "nom": "[hg] hg076 Wolverine (allie sans texte) : pose en jeu sous controle, aucun plantage",
        "pourquoi": "aucun texte imprime : fichier .py vide, tout est natif (ATK/THW/PV)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('hg076', under_control=True)"],
        "main_exclusive": ["01088"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["hg076"]},
    },
]


# ============================================================ Corrections du 27/10/2026 (audit GABARITS.md)
# Regles du livret sans carte, branchees par `commun.ReglesDuScenario` sur le Coeur (hg001-hg003) :
# jeton actif (p. 4), Metazombie vaincu (p. 3 + FAQ p. 8), Infection (p. 5). Les cas « rhino » posent hg001
# pour que ces regles soient enregistrees ; les cas « the_hunger_core » jouent la vraie mise en place (graine 42).
# Vaincre TOUS les Metazombies d'une vraie partie (tires au hasard : on ne peut pas les nommer) sans toucher au
# Coeur : `DamageAllVillains` passe par une regle de debug que Shielded by the Horde ne bloque pas (mesure le
# 27/10/2026 : le Coeur prenait les 99 degats et Deeper Inside partait). Une carte Tenace sur le Coeur absorbe ce
# coup-la ; il ne prend ensuite que Rupture (1 par Metazombie vaincu, solo).
TUER_LES_METAZOMBIES = ["Puzzle.AddTough('hg001')", "Puzzle.DamageAllVillains(99)"]

CAS += [
    # ------------------------------------------------------------ jeton actif
    {
        "nom": "[hg] regle jeton : apres la mise en place, le jeton est sur le PREMIER Metazombie de la rangee (pas sur le Coeur)",
        "pourquoi": "livret p. 7, etape 7 : « Put 2 Metazombies from the Horde deck into play ... Place the active Metazombie "
                    "token on the first one in the row. » Avant le correctif, hg004a laissait le jeton sur le Coeur : "
                    "aucun Metazombie ne s'activait jamais en phase du mechant.",
        "scenario": "the_hunger_core", "heros": "spider_man",
        "mise_en_place": [],
        "declencher": [],
        "verifier": "hg_jeton_etat",
        "attendu": {"actif_rang": 0, "n_metazombies": 2},
    },
    {
        "nom": "[hg] regle jeton : fin de phase du mechant -> le jeton passe au Metazombie SUIVANT a droite",
        "pourquoi": "« At the end of each villain phase, the token moves to the next Metazombie in the row, to the right. »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('hg001')", "Puzzle.PutIntoPlay('hg013')",
                          "Puzzle.PutIntoPlay('hg014')", "Puzzle.PutIntoPlay('hg009')", "Puzzle.SetActiveVillain('hg013')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EndVillainPhase()"],
        "verifier": "hg_jeton_etat",
        "attendu": {"actif": "hg014"},
    },
    {
        "nom": "[hg] regle jeton : fin de phase du mechant depuis le DERNIER Metazombie -> retour au premier",
        "pourquoi": "« From the last one it goes back to the first. »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('hg001')", "Puzzle.PutIntoPlay('hg013')",
                          "Puzzle.PutIntoPlay('hg014')", "Puzzle.PutIntoPlay('hg009')", "Puzzle.SetActiveVillain('hg009')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EndVillainPhase()"],
        "verifier": "hg_jeton_etat",
        "attendu": {"actif": "hg013"},
    },
    {
        "nom": "[hg] regle jeton TEMOIN : sans le Coeur en jeu (regles non enregistrees), la fin de phase ne deplace rien",
        "pourquoi": "preuve par substitution : la rotation vient bien de `ReglesDuScenario` (portee par le Coeur), pas du moteur",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('hg013')",
                          "Puzzle.PutIntoPlay('hg014')", "Puzzle.PutIntoPlay('hg009')", "Puzzle.SetActiveVillain('hg013')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EndVillainPhase()"],
        "verifier": "hg_jeton_etat",
        "attendu": {"actif": "hg013"},
    },
    {
        "nom": "[hg] regle Metazombie vaincu : le Metazombie ACTIF du milieu tombe -> jeton au suivant A DROITE, vaincu dans la defausse du Horde deck",
        "pourquoi": "« If the active Metazombie is defeated, the token moves immediately to the next one in the row » + « When a "
                    "Metazombie is defeated: ... put it in the Horde discard pile ». Rangee hg013, hg014, hg009 : hg014 actif "
                    "tombe -> hg009 (l'ancien code prenait le premier, hg013).",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('hg001')", "Puzzle.PutIntoPlay('hg013')",
                          "Puzzle.PutIntoPlay('hg014')", "Puzzle.PutIntoPlay('hg009')", "Puzzle.SetActiveVillain('hg014')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Damage('hg014', 99)"],
        "verifier": "hg_jeton_etat",
        "attendu": {"actif": "hg009", "horde_defausse": ["hg014"], "hors_jeu": ["hg014"]},
    },
    {
        "nom": "[hg] regle Metazombie vaincu : le DERNIER (actif) tombe -> jeton au premier de la rangee",
        "pourquoi": "« moves immediately to the next one in the row » + rotation circulaire (« From the last one it goes back to the first »)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('hg001')", "Puzzle.PutIntoPlay('hg013')",
                          "Puzzle.PutIntoPlay('hg014')", "Puzzle.PutIntoPlay('hg009')", "Puzzle.SetActiveVillain('hg009')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Damage('hg009', 99)"],
        "verifier": "hg_jeton_etat",
        "attendu": {"actif": "hg013", "horde_defausse": ["hg009"]},
    },
    {
        "nom": "[hg] regle Metazombie vaincu : un Metazombie NON actif tombe -> le jeton ne bouge pas",
        "pourquoi": "contre-cas : seul « the ACTIVE Metazombie is defeated » deplace le jeton",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('hg001')", "Puzzle.PutIntoPlay('hg013')",
                          "Puzzle.PutIntoPlay('hg014')", "Puzzle.PutIntoPlay('hg009')", "Puzzle.SetActiveVillain('hg013')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Damage('hg014', 99)"],
        "verifier": "hg_jeton_etat",
        "attendu": {"actif": "hg013", "horde_defausse": ["hg014"]},
    },
    {
        "nom": "[hg] regle Metazombie vaincu : ses attachements de signature vont au FOND de son deck signature (pas a la defausse)",
        "pourquoi": "FAQ p. 8 : « A Metazombie with attachments is defeated. What happens to them? They go to the bottom of its "
                    "signature deck. » Zombie Thor + Bloodied Mjolnir (hg034) : apres la defaite, hg034 est au fond du deck "
                    "signature de hg012 (3 cartes + celle-ci = 4).",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('hg001')", "Puzzle.PutIntoPlay('hg012')", "Puzzle.Reveal('hg034')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Damage('hg012', 99)"],
        "verifier": "hg_jeton_etat",
        "attendu": {"horde_defausse": ["hg012"], "fond_deck_signature": [["hg012", "hg034", 4]], "hors_jeu": ["hg034"]},
    },
    {
        "nom": "[hg] regle jeton (vraie partie) : les deux Metazombies tombent -> jeton sur le Coeur, les deux dans la defausse du Horde deck",
        "pourquoi": "« If no Metazombie is left, the token moves to The Hunger Core. » DamageAllVillains : le Coeur (blinde) "
                    "ne prend rien directement, chaque Metazombie tombe (Rupture 1 chacun).",
        "scenario": "the_hunger_core", "heros": "spider_man",
        "mise_en_place": [],
        "declencher": [*TUER_LES_METAZOMBIES],
        "verifier": "hg_jeton_etat",
        "attendu": {"actif": "hg001", "n_horde_defausse": 2, "n_metazombies": 0, "degats": [["hg001", 2]]},
    },
    {
        "nom": "[hg] regle jeton (vraie partie) : jeton sur le Coeur, un Metazombie RENTRE (Rise of the Horde!) -> le jeton passe sur lui",
        "pourquoi": "« When a Metazombie enters play again, the token moves to it. »",
        "scenario": "the_hunger_core", "heros": "spider_man",
        "mise_en_place": [*TUER_LES_METAZOMBIES],
        "declencher": ["Puzzle.Reveal('hg047')"],
        "verifier": "hg_jeton_etat",
        "attendu": {"actif_rang": 0, "n_metazombies": 1},
    },

    {
        "nom": "[hg] regle Metazombie vaincu (vraie partie) : Horde deck epuise -> sa defausse (les vaincus) est remelangee, des vaincus REVIENNENT indemnes",
        "pourquoi": "« If the Horde deck is empty, shuffle its discard pile to make a new one » + FAQ « If that Metazombie comes "
                    "back » : prouve que les vaincus vont bien dans la defausse du Horde deck (avant le correctif, ils etaient "
                    "retires de la partie et ne revenaient jamais). Graine 42, mesure etape par etape le 27/10/2026 : en jeu "
                    "hg011+hg015 ; 1re vague tuee (defausse 2) ; 3 entrees (hg014, hg012, hg007 : Horde deck a 3) ; 2e vague "
                    "tuee (defausse 5) ; 3 entrees qui VIDENT le Horde deck -> le Deck2 (BindDiscardPile) remelange "
                    "aussitot sa defausse (5 revenants) ; 3e vague tuee (defausse = hg008, hg009, hg013) ; les 2 Rise of the "
                    "Horde! suivants tirent donc forcement 2 des 5 REVENANTS, sans degats.",
        "scenario": "the_hunger_core", "heros": "spider_man",
        "mise_en_place": [*TUER_LES_METAZOMBIES,
                          "Puzzle.Reveal('hg047')", "Puzzle.Reveal('hg047')", "Puzzle.Reveal('hg047')", *TUER_LES_METAZOMBIES,
                          "Puzzle.Reveal('hg047')", "Puzzle.Reveal('hg047')", "Puzzle.Reveal('hg047')", *TUER_LES_METAZOMBIES,
                          "Puzzle.Reveal('hg047')"],
        "declencher": ["Puzzle.Reveal('hg047')"],
        "verifier": "hg_jeton_etat",
        "attendu": {"n_metazombies": 2, "n_horde_defausse": 3, "horde_defausse": ["hg008", "hg009", "hg013"],
                    "metazombies_indemnes": True, "actif_rang": 0},
    },

    {
        "nom": "[hg] regle jeton (vraie partie) : fin de phase du mechant -> le jeton avance d'UN SEUL cran (rang 0 -> rang 1)",
        "pourquoi": "« the token moves to the next Metazombie » : un seul pas. Garde-fou mesure en autoplay le 27/10/2026 : en "
                    "standard, hg002 (stade II, hors jeu dans le deck des stades) declenchait aussi la regle (type Scenario actif "
                    "hors jeu) et le jeton avancait de DEUX crans, retombant sur le premier avec 2 Metazombies.",
        "scenario": "the_hunger_core", "heros": "spider_man",
        "mise_en_place": [],
        "declencher": ["Puzzle.EndVillainPhase()"],
        "verifier": "hg_jeton_etat",
        "attendu": {"actif_rang": 1},
    },
    {
        "nom": "[hg] regle Infection (vraie partie) : une morsure de Metazombie -> UN SEUL compteur Infection (pas un par stade du Coeur)",
        "pourquoi": "« place 1 Infection counter » : meme garde-fou que le cas precedent (hg002 hors jeu doublait la pose). "
                    "Graine 42 : hg011 Zombie Captain Marvel (ATK 1) en jeu des la mise en place.",
        "scenario": "the_hunger_core", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS],
        "declencher": ["Puzzle.EnemyAttacks('hg011', '01001b')"],
        "passer_sur_option": "Defense",
        "verifier": "hg_jeton_etat",
        "attendu": {"compteurs_identite": [["infection", 1]]},
    },

    # ------------------------------------------------------------ Infection (regle de base, livret p. 5)
    {
        "nom": "[hg] regle Infection : l'attaque d'un METAZOMBIE blesse le heros -> 1 compteur Infection",
        "pourquoi": "« Infection. When an attack from a Zombie or Metazombie enemy deals damage to your hero, place 1 Infection counter. »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg001')", "Puzzle.PutIntoPlay('hg009')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EnemyAttacks('hg009', '01001b')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 4, "compteurs_identite": [["infection", 1]]},
    },
    {
        "nom": "[hg] regle Infection : l'attaque d'un sbire ZOMBIE (hg056) blesse le heros -> 1 compteur Infection",
        "pourquoi": "« a Zombie or Metazombie enemy » : le trait ZOMBIE des sbires Hungry Horde compte aussi",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg001')", "Puzzle.PutIntoPlay('hg056')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EnemyAttacks('hg056', '01001b')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 1, "compteurs_identite": [["infection", 1]]},
    },
    {
        "nom": "[hg] regle Infection contre-cas : le heros Tenace absorbe tout -> 0 degat, AUCUNE Infection",
        "pourquoi": "« if your DEF or a tough status card prevents all the damage, there is no Infection »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg001')", "Puzzle.PutIntoPlay('hg009')",
                          "Puzzle.Tough('01001b')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EnemyAttacks('hg009', '01001b')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0, "compteurs_identite": [["infection", 0]]},
    },
    {
        "nom": "[hg] regle Infection contre-cas : Rhino (ni Zombie ni Metazombie) blesse le heros -> AUCUNE Infection",
        "pourquoi": "« from a Zombie or Metazombie enemy » seulement",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg001')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EnemyAttacks('01094', '01001b')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2, "compteurs_identite": [["infection", 0]]},
    },
    {
        "nom": "[hg] regle Infection TEMOIN : meme attaque de Metazombie SANS le Coeur en jeu -> aucune Infection",
        "pourquoi": "preuve par substitution : l'Infection vient bien de `ReglesDuScenario`, portee par le Coeur",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg009')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EnemyAttacks('hg009', '01001b')"],
        "passer_sur_option": "Defense",
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 4, "compteurs_identite": [["infection", 0]]},
    },

    # ------------------------------------------------------------ Trapped Survivors dans le deck de rencontre
    {
        "nom": "[hg] hg051-hg055 mise en place : les 5 Trapped Survivor sont MELANGES au deck de rencontre (pas mis de cote)",
        "pourquoi": "livret p. 7, etape 6 : « The Hunger Core set (13 cards, with the remaining Trapped Survivors) »",
        "scenario": "the_hunger_core", "heros": "spider_man",
        "mise_en_place": [],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"dans_deck_rencontre": ["hg051", "hg052", "hg053", "hg054", "hg055"],
                    "mis_de_cote_scenario": ["hg072", "hg073", "hg074", "hg075", "hg076"]},
    },

    # ------------------------------------------------------------ hg003 (aucun cas jusqu'ici)
    {
        "nom": "[hg] hg003 When Revealed : chaque joueur pose 1 compteur Infection",
        "pourquoi": "« When Revealed: Each player places 1 infection counter. » (stade III)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('hg003')"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs_identite": [["infection", 1]]},
    },
    {
        "nom": "[hg] hg003 Just a Core 2 : le Coeur III expose active contre un heros -> 2 cartes face cachee, 0 degat",
        "pourquoi": "« Just a Core 2. Instead of attacking you, deal yourself 2 facedown encounter cards. » (valeur propre au stade III)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg003')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Activate('hg003')"],
        "verifier": "hg014_etat",
        "attendu": {"degats_identite": 0, "cartes_distribuees": 2},
    },

    # ------------------------------------------------------------ hg015 : branche « aucun sbire -> un Metazombie »
    {
        "nom": "[hg] hg015 Portal to Limbo : aucun sbire dans le deck de rencontre et moins de 3 Metazombies -> un Metazombie entre en jeu",
        "pourquoi": "« If no minion is discarded and there are fewer than 3 Metazombies in play, put a Metazombie into play. » "
                    "Vraie partie (Horde deck construit) : les 2 Metazombies de depart tombent d'abord, puis hg015 seul "
                    "active ; deck de rencontre sans sbire -> le Horde deck fournit le 2e.",
        "scenario": "the_hunger_core", "heros": "spider_man",
        "mise_en_place": [*TUER_LES_METAZOMBIES, FORME_HEROS, "Puzzle.PutIntoPlay('hg015')",
                          "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105')"],
        "declencher": ["Puzzle.Activate('hg015')"],
        "passer_sur_option": "Defense",
        "verifier": "hg_jeton_etat",
        "attendu": {"n_metazombies": 2},
    },
    {
        "nom": "[hg] hg015 TEMOIN : meme montage mais hg015 n'active pas -> un seul Metazombie en jeu",
        "pourquoi": "contre-cas : le 2e Metazombie du cas precedent vient bien de Portal to Limbo",
        "scenario": "the_hunger_core", "heros": "spider_man",
        "mise_en_place": [*TUER_LES_METAZOMBIES, FORME_HEROS, "Puzzle.PutIntoPlay('hg015')",
                          "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105')"],
        "declencher": [],
        "verifier": "hg_jeton_etat",
        "attendu": {"n_metazombies": 1},
    },

    {
        "nom": "[hg] hg015 Portal to Limbo PLAFOND : deja 3 Metazombies, aucun sbire -> aucun 4e Metazombie",
        "pourquoi": "« ... and there are FEWER THAN 3 Metazombies in play, put a Metazombie into play » : temoin de la limite. "
                    "Graine 42 : hg011 et hg015 en jeu apres la mise en place, Rise of the Horde! en ajoute un 3e.",
        "scenario": "the_hunger_core", "heros": "spider_man",
        "mise_en_place": ["Puzzle.Reveal('hg047')", FORME_HEROS,
                          "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105')"],
        "declencher": ["Puzzle.Activate('hg015')"],
        "passer_sur_option": "Defense",
        "verifier": "hg_jeton_etat",
        "attendu": {"n_metazombies": 3},
    },

    # ------------------------------------------------------------ hg034 : Overkill
    {
        "nom": "[hg] hg034 Overkill : Zombie Thor (ATK 3+1) abat Black Cat (2 PV) qui defend -> 2 degats d'exces a l'identite",
        "pourquoi": "« His attacks gain Overkill and Piercing. » + mots-cles/overkill.md (ennemi abat un allie -> exces au controleur)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg012')", "Puzzle.Reveal('hg034')",
                          "Puzzle.PutIntoPlay('01002', under_control=True)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EnemyAttacks('hg012', '01001b', defender='01002')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["01002"], "degats_identite": 2},
    },
    {
        "nom": "[hg] hg034 Overkill TEMOIN : MEME montage SANS Mjolnir (ATK 3) -> Black Cat meurt, AUCUN exces",
        "pourquoi": "preuve par substitution : l'Overkill vient de hg034, pas de Zombie Thor",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('hg012')",
                          "Puzzle.PutIntoPlay('01002', under_control=True)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EnemyAttacks('hg012', '01001b', defender='01002')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["01002"], "degats_identite": 0},
    },

    # ------------------------------------------------------------ hg066 : plafond de 2 Tenaces
    {
        "nom": "[hg] hg066 plafond : revele (2 Tenaces), une 3e Tenace est REFUSEE -> toujours 2",
        "pourquoi": "« It can have 2 tough status cards at the same time » : 2, pas plus (ThisCanHaveAdditionalTough(1))",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.Reveal('hg066')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.AddTough('hg066')"],
        "verifier": "hg_etat_plus",
        "attendu": {"tenaces": [["hg066", 2]]},
    },
]

# Trapped Survivor « At 3 counters » : un cas PAR carte (hg051 a deja le sien plus haut), preuve que chaque fichier
# retire le BON allie au seuil.
for _sch, _allie, _nom in (("hg052", "hg073", "Chewie"), ("hg053", "hg074", "Valeria Richards"),
                           ("hg054", "hg075", "Blade"), ("hg055", "hg076", "Wolverine")):
    CAS.append({
        "nom": f"[hg] {_sch} A 3 COMPTEURS : la manigance ET {_nom} ({_allie}, mis de cote) sont retires du jeu, 1 infection par joueur",
        "pourquoi": f"« At 3 counters, remove this card and {_nom} from the game; each player places 1 infection counter. »",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, f"Puzzle.PutIntoPlay('{_sch}')", f"Puzzle.Counter('{_sch}', 'counter', 2)",
                          f"Puzzle.MoveTo('{_allie}', 'AsideScenario')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.RunVillainPhase()"],
        "verifier": "hg_etat_plus",
        "attendu": {"retires": [_sch, _allie], "compteurs_identite": [["infection", 1]]},
    })

VERIFICATIONS = r'''
def hg_setup_etat(monde, aides):
    """Verificateur dedie a la mise en place (hg004a) : contenu du Horde deck (deck + defausse + en jeu, un
    stock que `etat_attendu` ne sait pas lire) et cartes retirees du jeu (Survivor homonyme)."""
    from game.card.face.base import Villain
    attendu = aides["cas"].get("attendu") or {}
    soucis = []

    scenario = monde.GetScenario()
    horde_deck = getattr(scenario, "hgc_horde_deck", None)
    horde_discard = getattr(scenario, "hgc_horde_discard", None)
    horde_ids = set()
    if horde_deck is not None:
        horde_ids |= {f.paper.card_id for f in horde_deck.Get(True)}
    if horde_discard is not None:
        horde_ids |= {f.paper.card_id for f in horde_discard.Get(True)}

    metazombies_en_jeu = []
    for objet in monde.object_manager.card_dict.values():
        face = objet.face
        if face is None or not isinstance(face, Villain) or not face.IsInPlay():
            continue
        if face.HasTrait("METAZOMBIE"):
            metazombies_en_jeu.append(face.paper.card_id)
            horde_ids.add(face.paper.card_id)

    if "villain_en_jeu" in attendu:
        trouve = any(isinstance(o.face, Villain) and o.face.IsInPlay() and o.face.paper.card_id == attendu["villain_en_jeu"]
                     for o in monde.object_manager.card_dict.values())
        if not trouve:
            soucis.append(f"{attendu['villain_en_jeu']} introuvable en jeu")

    if "n_metazombies" in attendu and len(metazombies_en_jeu) != attendu["n_metazombies"]:
        soucis.append(f"Metazombies en jeu = {len(metazombies_en_jeu)} {sorted(metazombies_en_jeu)} (attendu {attendu['n_metazombies']})")

    if "horde_total" in attendu and len(horde_ids) != attendu["horde_total"]:
        soucis.append(f"Horde deck+defausse+en jeu = {len(horde_ids)} {sorted(horde_ids)} (attendu {attendu['horde_total']})")

    if attendu.get("horde_absent"):
        if attendu["horde_absent"] in horde_ids:
            soucis.append(f"{attendu['horde_absent']} est dans le Horde deck (ne devrait jamais y etre)")

    for card_id in attendu.get("retires") or []:
        dans_les_retires = any(getattr(f.paper, "card_id", None) == card_id
                               for f in monde.area_removed.Get(True))
        if not dans_les_retires:
            soucis.append(f"{card_id} n'est pas dans les cartes retirees du jeu")

    if soucis:
        return False, " ; ".join(soucis)
    return True, "etat conforme"
'''

VERIFICATIONS += r'''
def hg_distribuees_et_pas_de_degats(monde, aides):
    """« that player deals themself X facedown encounter cards » : AUCUNE cle generique de etat_attendu ne compte
    les cartes de rencontre distribuees (dealt_encounter_cards), d'ou ce petit verificateur dedie."""
    identite = aides["identite"](monde)
    joueur = monde.players[0]
    distribuees = joueur.dealt_encounter_cards.Get(True)
    if identite.max_health - identite.health != 0:
        return False, f"degats sur l'identite = {identite.max_health - identite.health} (attendu 0)"
    if len(distribuees) < 1:
        return False, f"aucune carte de rencontre distribuee au joueur (attendu au moins 1)"
    return True, f"{len(distribuees)} carte(s) de rencontre distribuee(s), 0 degat sur l'identite"
'''

VERIFICATIONS += r'''
def hg_manigance_etat(monde, aides):
    """Verificateur dedie a la manigance principale (hg004b/hg005a/hg005b) : `complot` (card_id de la face EN JEU
    dans area_schemes_main), `mechant` (card_id de « The Hunger Core », quel que soit son stade, ou None si
    absent/vaincu), `n_metazombies` (Metazombies vivants en jeu), `environnement_en_jeu` (nom d'un environnement
    en jeu) et `fin` (None | "gagne" | "perdu"), modele `ap_etat` (alien_vs_predator.py)."""
    from game.operate.worlds import Worlds
    from game.card.face.base import Villain
    from game.card.face.card_type import Environment
    from game.effect.rule import GameRule

    attendu = aides["cas"].get("attendu") or {}
    soucis = []
    cid = lambda f: getattr(getattr(f, "paper", None), "card_id", None)

    effet = GameRule(monde.const_seat_order_players[0].GetIdentity())
    complots = [c for c in Worlds.GetAllMainSchemes(monde) if c.IsInPlay()]
    coeur = next((v for v in Worlds.GetVillains(effet) if v.IsName("The Hunger Core") and v.IsInPlay()), None)
    metazombies = [v for v in Worlds.GetVillains(effet) if v.HasTrait("METAZOMBIE") and v.IsInPlay()]

    mesures = {
        "complot": cid(complots[0]) if complots else None,
        "mechant": cid(coeur),
        "n_metazombies": len(metazombies),
        "fin": (None if not monde.is_game_over else ("gagne" if monde.game_over.players_won else "perdu")),
    }

    if "complot" in attendu and mesures["complot"] != attendu["complot"]:
        soucis.append(f"complot en jeu = {mesures['complot']} (attendu {attendu['complot']})")
    if "mechant" in attendu and mesures["mechant"] != attendu["mechant"]:
        soucis.append(f"mechant « The Hunger Core » en jeu = {mesures['mechant']} (attendu {attendu['mechant']})")
    if "n_metazombies" in attendu and mesures["n_metazombies"] != attendu["n_metazombies"]:
        soucis.append(f"Metazombies en jeu = {mesures['n_metazombies']} {sorted(cid(v) for v in metazombies)} (attendu {attendu['n_metazombies']})")
    if "fin" in attendu and mesures["fin"] != attendu["fin"]:
        soucis.append(f"fin de partie = {mesures['fin']} (attendu {attendu['fin']})")
    if "environnement_en_jeu" in attendu:
        trouve = any(isinstance(o.face, Environment) and o.face.IsInPlay() and o.face.IsName(attendu["environnement_en_jeu"])
                     for o in monde.object_manager.card_dict.values())
        if not trouve:
            soucis.append(f"environnement « {attendu['environnement_en_jeu']} » introuvable en jeu")

    if soucis:
        return False, " ; ".join(soucis)
    return True, f"etat conforme : {mesures}"
'''

VERIFICATIONS += r'''
def hg_peut_defendre_etat(monde, aides):
    """Verificateur dedie a hg013 Zombie Black Widow : `peut_defendre` ([[defenseur, attaquant, bool]], modele
    `ap_etat`/alien_vs_predator.py) mesure `IsCanDefense`, la legalite que le moteur consulte AVANT d'offrir la
    defense -- pas le resultat d'une attaque deja resolue par le defenseur impose par le harnais."""
    attendu = aides["cas"].get("attendu") or {}
    soucis = []
    for defenseur, attaquant, voulu in attendu.get("peut_defendre") or []:
        d, a = aides["par_id"](monde, defenseur), aides["par_id"](monde, attaquant)
        peut = d.IsCanDefense(a) if d is not None and a is not None else None
        if peut != voulu:
            soucis.append(f"{defenseur} peut defendre contre {attaquant} = {peut} (attendu {voulu})")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "etat conforme"
'''

VERIFICATIONS += r'''
def hg008_deck_signature_etat(monde, aides):
    """Verificateur dedie : taille du deck signature d'un Metazombie (stocke en attribut dynamique sur
    `metazombie.card`, cle `_hgc_sig_<id>`, voir `commun.DeckSignatureDe`). `taille_deck_signature` dans
    `attendu` est compare a `deck.GetSize()`."""
    attendu = aides["cas"].get("attendu") or {}
    face = aides["par_id"](monde, "hg008")
    if face is None:
        return False, "hg008 introuvable en jeu"

    deck = None
    for cle, valeur in vars(face.card).items():
        if cle.startswith("_hgc_sig_"):
            deck = valeur
            break
    if deck is None:
        return False, "deck signature introuvable sur hg008 (jamais consulte ?)"

    taille = deck.GetSize()
    if "taille_deck_signature" in attendu and taille != attendu["taille_deck_signature"]:
        return False, f"deck signature de hg008 = {taille} carte(s) (attendu {attendu['taille_deck_signature']})"
    return True, f"deck signature de hg008 = {taille} carte(s)"
'''

VERIFICATIONS += r'''
def hg014_etat(monde, aides):
    """Verificateur dedie a hg014 Zombie Doctor Strange (Hex) : cumule degats_identite et cartes_distribuees
    (joueur 0), modele hg_distribuees_et_pas_de_degats adapte au fait que CETTE carte NE remplace PAS
    l'attaque (contrairement a Just a Core) : l'activation inflige les degats normaux ET distribue en plus
    la carte de rencontre."""
    identite = aides["identite"](monde)
    joueur = monde.players[0]
    attendu = aides["cas"].get("attendu") or {}
    soucis = []
    degats = identite.max_health - identite.health
    if "degats_identite" in attendu and degats != attendu["degats_identite"]:
        soucis.append(f"degats identite = {degats} (attendu {attendu['degats_identite']})")
    distribuees = joueur.dealt_encounter_cards.Get(True)
    if "cartes_distribuees" in attendu and len(distribuees) != attendu["cartes_distribuees"]:
        soucis.append(f"cartes de rencontre distribuees = {len(distribuees)} (attendu {attendu['cartes_distribuees']})")
    if soucis:
        return False, " ; ".join(soucis)
    return True, f"degats identite={degats}, cartes distribuees={len(distribuees)}"
'''

VERIFICATIONS += r'''
def hg_etat_plus(monde, aides):
    """Verificateur dedie hg028-hg076 (fusion du 27/10/2026), pour ce que `etat_attendu` ne sait pas lire, puis
    delegation a `etat_attendu` pour toutes les autres cles :
    - `retires` : [card_id] -> chaque carte est dans les cartes RETIREES DU JEU (area_removed) ;
    - `deck_signature` : [[metazombie_id, taille|None]] -> taille du deck signature (attribut `_hgc_sig_` pose sur
      `metazombie.card` par `commun.DeckSignatureDe`) ; None = ce deck n'a JAMAIS ete consulte ;
    - `n_metazombies` : nombre de Metazombies (vilains au trait METAZOMBIE) vivants en jeu ;
    - `metazombie_demi_pv` : exactement UN Metazombie en jeu est blesse, et de max_health // 2 (hg048) ;
    - `tenaces` : [[card_id, n]] -> nombre de cartes d'etat Tenace sur la carte."""
    from game.card.face.base import Villain
    attendu = aides["cas"].get("attendu") or {}
    soucis = []

    for card_id in attendu.get("retires") or []:
        if not any(getattr(f.paper, "card_id", None) == card_id for f in monde.area_removed.Get(True)):
            soucis.append(f"{card_id} n'est pas dans les cartes retirees du jeu")

    for card_id, taille in attendu.get("deck_signature") or []:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable en jeu (deck_signature)")
            continue
        deck = next((v for k, v in vars(face.card).items() if k.startswith("_hgc_sig_")), None)
        reel = None if deck is None else deck.GetSize()
        if reel != taille:
            soucis.append(f"deck signature de {card_id} = {reel} (attendu {taille})")

    metazombies = [o.face for o in monde.object_manager.card_dict.values()
                   if o.face is not None and isinstance(o.face, Villain) and o.face.IsInPlay()
                   and o.face.HasTrait("METAZOMBIE")]
    if "n_metazombies" in attendu and len(metazombies) != attendu["n_metazombies"]:
        soucis.append(f"Metazombies en jeu = {len(metazombies)} (attendu {attendu['n_metazombies']})")
    if attendu.get("metazombie_demi_pv"):
        blesses = [(f.paper.card_id, f.max_health - f.health, f.max_health) for f in metazombies if f.max_health - f.health > 0]
        if len(blesses) != 1 or blesses[0][1] != blesses[0][2] // 2:
            soucis.append(f"Metazombies blesses (id, degats, PV max) = {blesses} (attendu un seul, a PV max // 2)")

    for card_id, n in attendu.get("tenaces") or []:
        face = aides["par_id"](monde, card_id)
        reel = None if face is None else getattr(face, "tough", None)
        if reel != n:
            soucis.append(f"{card_id} porte {reel} carte(s) Tenace (attendu {n})")

    ok, message = etat_attendu(monde, aides)
    if not ok:
        soucis.append(message)
    if soucis:
        return False, " ; ".join(soucis)
    return True, "etat conforme"
'''

VERIFICATIONS += r'''
def hg_jeton_etat(monde, aides):
    """Verificateur des regles de scenario (27/10/2026, `commun.ReglesDuScenario`), puis delegation a `etat_attendu` :
    - `actif` : card_id du mechant qui porte le compteur 'active' (None = personne) ;
    - `actif_rang` : le porteur est le Metazombie de ce rang dans la rangee (0 = le premier) ;
    - `n_metazombies` : Metazombies (vilains METAZOMBIE) vivants en jeu ;
    - `horde_defausse` : [card_id] presents dans la defausse du Horde deck ; `n_horde_defausse` : sa taille ;
    - `fond_deck_signature` : [[metazombie_id, card_id, taille]] -> la carte est AU FOND du deck signature du
      Metazombie (cherche partout, il peut etre hors jeu) et ce deck a cette taille."""
    from game.card.face.base import Villain
    attendu = aides["cas"].get("attendu") or {}
    soucis = []
    cid = lambda f: getattr(getattr(f, "paper", None), "card_id", None)

    mechants = [o.face for o in monde.object_manager.card_dict.values()
                if o.face is not None and isinstance(o.face, Villain) and o.face.IsInPlay()]
    from game.operate.worlds import Worlds
    from game.effect.rule import GameRule
    rangee_ordonnee = [v for v in Worlds.GetVillains(GameRule(monde.const_seat_order_players[0].GetIdentity()))
                       if v.HasTrait("METAZOMBIE") and v.IsInPlay()]
    actifs = [m for m in mechants if m.GetCounters('active') > 0]
    actif = actifs[0] if actifs else None
    if len(actifs) > 1:
        soucis.append(f"plusieurs porteurs du jeton : {[cid(a) for a in actifs]}")
    if "actif" in attendu and cid(actif) != attendu["actif"]:
        soucis.append(f"jeton actif sur {cid(actif)} (attendu {attendu['actif']})")
    if "actif_rang" in attendu:
        r = attendu["actif_rang"]
        voulu = rangee_ordonnee[r] if r < len(rangee_ordonnee) else None
        if voulu is None or actif is not voulu:
            soucis.append(f"jeton actif sur {cid(actif)}, rangee = {[cid(v) for v in rangee_ordonnee]} (attendu rang {r})")
    if "n_metazombies" in attendu and len(rangee_ordonnee) != attendu["n_metazombies"]:
        soucis.append(f"Metazombies en jeu = {[cid(v) for v in rangee_ordonnee]} (attendu {attendu['n_metazombies']})")

    defausse = getattr(monde.GetScenario(), "hgc_horde_discard", None)
    ids_defausse = [cid(f) for f in defausse.Get(True)] if defausse is not None else []
    for card_id in attendu.get("horde_defausse") or []:
        if card_id not in ids_defausse:
            soucis.append(f"{card_id} absent de la defausse du Horde deck ({ids_defausse})")
    if "n_horde_defausse" in attendu and len(ids_defausse) != attendu["n_horde_defausse"]:
        soucis.append(f"defausse du Horde deck = {ids_defausse} (attendu {attendu['n_horde_defausse']} cartes)")

    for mz_id, card_id, taille in attendu.get("fond_deck_signature") or []:
        mz = next((o for o in monde.object_manager.card_dict.values()
                   if o.face is not None and cid(o.face) == mz_id
                   and any(k.startswith("_hgc_sig_") for k in vars(o))), None)
        if mz is None:
            soucis.append(f"{mz_id} : aucun deck signature trouve")
            continue
        deck = next(v for k, v in vars(mz).items() if k.startswith("_hgc_sig_"))
        cartes = list(deck.Get(True))
        if deck.GetSize() != taille:
            soucis.append(f"deck signature de {mz_id} = {deck.GetSize()} (attendu {taille})")
        ids = [cid(f) for f in cartes]
        if card_id not in ids:
            soucis.append(f"{card_id} absent du deck signature de {mz_id} ({ids})")
        else:
            # fond = la carte qui sortirait en DERNIER : `GetTop` lit l'autre extremite.
            dessus = deck.GetTop()
            fond = cartes[0] if cartes and cartes[-1] is dessus else cartes[-1]
            if cid(fond) != card_id:
                soucis.append(f"fond du deck signature de {mz_id} = {cid(fond)}, dessus = {cid(dessus)} (attendu {card_id} au fond), ordre {ids}")

    if attendu.get("metazombies_indemnes"):
        blesses = [(cid(v), v.max_health - v.health, v.max_health) for v in rangee_ordonnee
                   if v.max_health - v.health != 0 or v.max_health <= 0]
        if blesses:
            soucis.append(f"Metazombies blesses ou sans PV (id, degats, PV max) = {blesses} (attendu tous indemnes)")

    cles_generiques = {k: v for k, v in attendu.items()
                       if k not in ("actif", "actif_rang", "n_metazombies", "horde_defausse", "n_horde_defausse",
                                    "fond_deck_signature", "metazombies_indemnes")}
    if cles_generiques:
        aides["cas"]["attendu"] = cles_generiques
        try:
            ok, message = etat_attendu(monde, aides)
        finally:
            aides["cas"]["attendu"] = attendu
        if not ok:
            soucis.append(message)
    pioche = getattr(monde.GetScenario(), "hgc_horde_deck", None)
    ids_pioche = [cid(f) for f in pioche.Get(True)] if pioche is not None else []
    if soucis:
        soucis.append(f"(Horde deck = {ids_pioche}, rangee = {[cid(v) for v in rangee_ordonnee]})")
        return False, " ; ".join(soucis)
    return True, (f"etat conforme (jeton sur {cid(actif)}, rangee {[cid(v) for v in rangee_ordonnee]}, "
                  f"Horde deck {ids_pioche}, defausse Horde {ids_defausse})")
'''

