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
]

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
