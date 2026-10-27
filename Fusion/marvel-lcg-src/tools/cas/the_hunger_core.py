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
