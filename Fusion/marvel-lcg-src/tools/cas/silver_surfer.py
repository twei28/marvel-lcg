# Cas test_capacites du heros custom SILVER SURFER (DesignHacker, MC4 SEALED, prefixe `sv`) :
# noms prefixes « [sv] » puis le card_id (substituer_pack.py filtre dessus).
#
# Rappels de montage :
#  - Silver Surfer demarre en ALTER EGO (sv001b Norrin Radd) ; `Puzzle.ChangeToFace('sv001b', 'sv001a')` la
#    passe en forme HEROS ;
#  - `player_deck` est VIDE dans le deck de depart (pas de decklist d'aspect fournie) : le harnais le complete
#    avec des ressources inertes, `main_exclusive` fixe la main ;
#  - Rhino 01094 est le vilain, 01097b son complot principal, 01101 Hydra Mercenary un sbire ;
#  - ressources : 01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR ; sv010 The Power Cosmic = YY.
SC = "rhino"
HEROS = "Puzzle.ChangeToFace('sv001b', 'sv001a')"
CIVIL = "Puzzle.ChangeToFace('sv001a', 'sv001b')"
SANS_DECK = "Puzzle.EmptyPlayerDeck()"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01105', '01105', '01105', '01105')"]
VIDER_DEFAUSSE = "Puzzle.EmptyPlayerDiscardPile()"
COMPLOT = "01097b"
VILAIN = "01094"


def en_jeu(*ids):
    return [f"Puzzle.PutIntoPlay('{i}', under_control=True)" for i in ids]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    if not cle.pop("avec_boost", False):
        mise = SANS_BOOST + list(mise)
    cas = {"nom": "[sv] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "silver_surfer"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "etat_attendu"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    # ============================================================ sv001a Silver Surfer : Compunction
    _c("sv001a Compunction : apres son attaque de base, la forme change (Hero -> AlterEgo)",
       "« Forced Response: After Silver Surfer makes a basic attack, change your form »",
       [HEROS], ["Puzzle.Attack('sv001a')"], {"forme": "AlterEgo", "degats": [[VILAIN, 3]]},
       main_exclusive=["01090"]),
    _c("sv001a Silver Surfer : valeurs imprimees PV 14, AERIAL COSMIC ADVENTURER",
       "nombres texte <-> code (scan 1A) : HAND SIZE 5 / HIT POINTS 14",
       [HEROS], [], {"pv_max": [["sv001a", 14]], "traits": ["AERIAL", "COSMIC", "ADVENTURER"]},
       main_exclusive=["01090"]),
    # ============================================================ sv001b Norrin Radd : Toomie!
    _c("sv001b Toomie! : cherche The Silver Surfboard dans le DECK et l'ajoute a la main (aucune autre carte prise)",
       "« search your deck and discard pile for The Silver Surfboard upgrade and add it to your hand »",
       [SANS_DECK, "Puzzle.CreatePlayerDeck('01090', 'sv003', '01089')"], ["Puzzle.Action('sv001b', 'Action')"],
       {"en_main": ["sv003"], "exhausted": ["sv001b"], "dans_deck_joueur": ["01089"]}, main_exclusive=["01090"]),
    _c("sv001b Toomie! : cherche aussi dans la DEFAUSSE (contre-cas : planche seulement defaussee)",
       "« deck AND discard pile » : sans la defausse, une planche defaussee serait perdue",
       [SANS_DECK, "Puzzle.CreatePlayerDeck('01090', '01089')", VIDER_DEFAUSSE, "Puzzle.CreatePlayerDiscardPile('sv003')"],
       ["Puzzle.Action('sv001b', 'Action')"],
       {"en_main": ["sv003"], "exhausted": ["sv001b"]}, main_exclusive=["01090"]),
    _c("sv001b Toomie! : alter-ego deja inclinee -> pas de recherche (le cout n'est pas payable)",
       "« Exhaust Norrin Radd -> » : la fleche en fait un COUT",
       [SANS_DECK, "Puzzle.CreatePlayerDeck('01090', 'sv003')", "Puzzle.Exhaust('sv001b')"], [],
       {"absent_main": ["sv003"]}, main_exclusive=["01090"],
       declencher_tolerant=["Puzzle.Action('sv001b', 'Action')"]),
    _c("sv001b Toomie! : absente en forme HEROS (aucune recherche)",
       "contre-cas dans l'AUTRE forme : l'Action est imprimee sur Norrin Radd",
       [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01090', 'sv003')"], [],
       {"absent_main": ["sv003"]}, main_exclusive=["01090"],
       declencher_tolerant=["Puzzle.Action('sv001a', 'Action')"]),
    _c("sv001b Norrin Radd : valeurs imprimees PV 14, COSMIC ADVENTURER",
       "nombres texte <-> code (scan 1B) : HAND SIZE 6 / HIT POINTS 14 / REC 4",
       [], [], {"pv_max": [["sv001b", 14]], "traits": ["COSMIC", "ADVENTURER"]}, main_exclusive=["01090"]),

    # ============================================================ sv002 Dawn Greenwood
    _c("sv002 Dawn Greenwood : vaincue, elle retourne en main contre 2 degats a l'identite",
       "« Interrupt: When Dawn Greenwood is defeated, deal 2 damage to your identity -> return Dawn Greenwood to your hand »",
       [HEROS, *en_jeu("sv002")], ["Puzzle.Defend('sv002', '01094')"],
       {"en_main": ["sv002"], "degats_identite": 2, "hors_jeu": ["sv002"]}, main_exclusive=["01090"], accepter_choix=True),
    _c("sv002 Dawn Greenwood : valeurs imprimees PV 1, cout 0, ADVENTURER",
       "nombres texte <-> code (scan) : cout 0, PV 1, ATK 1*, THW 1*",
       [HEROS, *en_jeu("sv002")], [], {"pv_max": [["sv002", 1]], "traits": [], "traits_de": [["sv002", "ADVENTURER"]]},
       main_exclusive=["01090"]),
    # ============================================================ sv003 The Silver Surfboard
    _c("sv003 The Silver Surfboard : Hero Action, incline la planche et redresse Silver Surfer",
       "« Hero Action: Exhaust The Silver Surfboard -> ready Silver Surfer »",
       [HEROS, *en_jeu("sv003"), "Puzzle.Exhaust('sv001a')"], ["Puzzle.Action('sv003', 'HeroAction')"],
       {"pret": ["sv001a"], "exhausted": ["sv003"]}, main_exclusive=["01090"]),
    _c("sv003 The Silver Surfboard : defaussee, 1 degat a Silver Surfer et on pioche 1 carte",
       "« Interrupt: When you discard The Silver Surfboard, deal 1 damage to Silver Surfer -> draw a card »",
       [HEROS, *en_jeu("sv003"), SANS_DECK, "Puzzle.CreatePlayerDeck('01089', '01089', '01089')"],
       ["Puzzle.Discard('sv003')"],
       {"degats_identite": 1, "taille_main": 2, "defausse": ["sv003"]}, main_exclusive=["01090"], accepter_choix=True),
    _c("sv003 The Silver Surfboard : defaussee en ALTER-EGO, le cout n'est pas payable (aucune pioche)",
       "lecture litterale : « Silver Surfer » est la face HEROS, absente en alter-ego",
       [*en_jeu("sv003"), SANS_DECK, "Puzzle.CreatePlayerDeck('01089', '01089', '01089')"],
       ["Puzzle.Discard('sv003')"],
       {"degats_identite": 0, "taille_main": 1, "defausse": ["sv003"]}, main_exclusive=["01090"], accepter_choix=True),
    _c("sv003 The Silver Surfboard : absente en ALTER-EGO (Hero Action inutilisable)",
       "contre-cas dans l'AUTRE forme : une Hero Action n'existe qu'en forme heros",
       [*en_jeu("sv003")], [], {"pret": ["sv003"]}, main_exclusive=["01090"],
       declencher_tolerant=["Puzzle.Action('sv003', 'HeroAction')"]),
    # ============================================================ sv004 Energy Manipulation
    _c("sv004 Energy Manipulation : Action, depenser Energy (YY) pose 2 compteurs energy",
       "« Action: Spend X [energy] resources -> put X energy counters here » (X = 2, Energy 01088)",
       [HEROS, *en_jeu("sv004")], ["Puzzle.Action('sv004', 'Action')"],
       {"compteurs": [["sv004", "energy", 2]]}, main_exclusive=["01088"], payer_avec=["01088"]),
    _c("sv004 Energy Manipulation : Hero Action, defausse et pioche 1 carte par compteur (3 compteurs -> 3 cartes)",
       "« Discard -> draw 1 card (to a maximum of 5) for each energy counter here »",
       [HEROS, *en_jeu("sv004"), "Puzzle.PlaceCounters('sv004', 'energy', 3)", SANS_DECK,
        "Puzzle.CreatePlayerDeck('01089', '01089', '01089', '01089', '01089', '01089')"],
       ["Puzzle.Action('sv004', 'HeroAction')"],
       {"taille_main": 4, "defausse": ["sv004"]}, main_exclusive=["01090"]),
    _c("sv004 Energy Manipulation : plafond de 5 cartes (7 compteurs -> 5 cartes)",
       "« (to a maximum of 5) » : le plafond porte sur les cartes piochees",
       [HEROS, *en_jeu("sv004"), "Puzzle.PlaceCounters('sv004', 'energy', 7)", SANS_DECK,
        "Puzzle.CreatePlayerDeck('01089', '01089', '01089', '01089', '01089', '01089', '01089', '01089')"],
       ["Puzzle.Action('sv004', 'HeroAction')"],
       {"taille_main": 6, "defausse": ["sv004"]}, main_exclusive=["01090"]),
    _c("sv004 Energy Manipulation : sans compteur, Hero Action = defausse sans pioche",
       "0 compteur -> 0 carte, la carte est tout de meme defaussee (cout)",
       [HEROS, *en_jeu("sv004"), SANS_DECK, "Puzzle.CreatePlayerDeck('01089', '01089', '01089')"],
       ["Puzzle.Action('sv004', 'HeroAction')"],
       {"taille_main": 1, "defausse": ["sv004"]}, main_exclusive=["01090"]),
    _c("sv004 Energy Manipulation : Hero Action absente en ALTER-EGO",
       "contre-cas dans l'AUTRE forme",
       [*en_jeu("sv004"), "Puzzle.PlaceCounters('sv004', 'energy', 3)", SANS_DECK, "Puzzle.CreatePlayerDeck('01089', '01089', '01089')"],
       [], {"taille_main": 1, "compteurs": [["sv004", "energy", 3]]}, main_exclusive=["01090"],
       declencher_tolerant=["Puzzle.Action('sv004', 'HeroAction')"]),
    # ============================================================ sv005 Rage of Retribution
    _c("sv005 Rage of Retribution : Silver Surfer a riposte 1 (Rhino qui l'attaque prend 1 degat)",
       "« Silver Surfer gains retaliate 1 »",
       [HEROS, *en_jeu("sv005")], ["Puzzle.Defend('sv001a', '01094')"],
       {"degats": [[VILAIN, 1]]}, main_exclusive=["01090"]),
    _c("sv005 Rage of Retribution : en ALTER-EGO, pas de riposte (Norrin Radd n'est pas Silver Surfer)",
       "contre-cas dans l'AUTRE forme : un NOM PROPRE ne designe que la face heros",
       [*en_jeu("sv005")], ["Puzzle.Attack('01094')"],
       {"degats": [[VILAIN, 0]]}, main_exclusive=["01090"]),
    _c("sv005 Rage of Retribution : au changement de forme, defaussee pour redresser Silver Surfer a la place",
       "« When Silver Surfer would change form, discard Rage of Retribution -> ready Silver Surfer instead »",
       [HEROS, *en_jeu("sv005")], ["Puzzle.Attack('sv001a')"],
       {"forme": "Hero", "pret": ["sv001a"], "defausse": ["sv005"]}, main_exclusive=["01090"], accepter_choix=True),
    # ============================================================ sv010 The Power Cosmic
    _c("sv010 The Power Cosmic : depensee pour un evenement COSMIC (Cosmic Speed), 2 degats a un ennemi",
       "« Response: After you spend this card to play a COSMIC event, deal 2 damage to an enemy »",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)"], [],
       {"degats": [[VILAIN, 2]], "menace": [[COMPLOT, 1]], "defausse": ["sv010", "sv006"]},
       main_exclusive=["sv006", "sv010", "01090"], payer_avec=["sv010", "01090"], jouer=["sv006"],
       cibles=[COMPLOT, VILAIN], choisir_option="Remove_4_threat_from_a_scheme"),
    _c("sv010 The Power Cosmic : depensee pour un evenement NON cosmique (Haymaker), pas de degats en plus",
       "contre-cas : Haymaker (ATTACK, pas COSMIC) fait ses 3 degats, rien de plus",
       [HEROS], [], {"degats": [[VILAIN, 3]], "defausse": ["sv010", "01087"]},
       main_exclusive=["01087", "sv010"], payer_avec=["sv010"], jouer=["01087"], cibles=[VILAIN]),

    # ============================================================ sv006 Cosmic Speed
    _c("sv006 Cosmic Speed : option 1, retire 4 menaces a une manigance (6 -> 2)",
       "« Remove 4 threat from a scheme »",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 6)"], [],
       {"menace": [[COMPLOT, 2]], "defausse": ["sv006"]},
       main_exclusive=["sv006", "01088", "01090"], payer_avec=["01088", "01090"], jouer=["sv006"], cibles=[COMPLOT],
       preferer_option="Remove 4 threat"),
    _c("sv006 Cosmic Speed : option 2, defausse la planche et retire jusqu'a 3 menaces de CHAQUE manigance",
       "« Discard The Silver Surfboard -> remove up to 3 threat from each scheme in play » : principal 5 -> 2, annexe 2 -> 0",
       [HEROS, *en_jeu("sv003"), f"Puzzle.SetThreat('{COMPLOT}', 5)", "Puzzle.Reveal('01107')"], [],
       {"menace": [[COMPLOT, 2]], "hors_jeu": ["01107"], "defausse": ["sv006", "sv003"]},
       main_exclusive=["sv006", "01088", "01090"], payer_avec=["01088", "01090"], jouer=["sv006"],
       preferer_option="Discard The Silver Surfboard"),
    _c("sv006 Cosmic Speed : sans planche en jeu, seule l'option 1 existe (menace 6 -> 2, aucune autre perte)",
       "la 2e option n'est pas offerte sans planche : on retire bien 4 et pas 3 par manigance",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 6)", "Puzzle.Reveal('01107')"], [],
       {"menace": [[COMPLOT, 2], ["01107", 3]], "defausse": ["sv006"]},
       main_exclusive=["sv006", "01088", "01090"], payer_avec=["01088", "01090"], jouer=["sv006"], cibles=[COMPLOT],
       preferer_option="Discard The Silver Surfboard"),
    # ============================================================ sv007 Cosmic Strength
    _c("sv007 Cosmic Strength : option 1, +7 ATQ pour l'attaque de base (3 + 7 = 10 degats a Rhino)",
       "« You get +7 ATK for that attack »",
       [HEROS], ["Puzzle.Attack('sv001a')"],
       {"degats": [[VILAIN, 10]], "defausse": ["sv007"]},
       main_exclusive=["sv007", "01088", "01090"], payer_avec=["01088", "01090"], preferer_option="+7 ATK"),
    _c("sv007 Cosmic Strength : option 2, defausse la planche -> +9 ATQ (3 + 9 = 12 degats a Rhino)",
       "« Discard The Silver Surfboard -> +9 ATK for that attack and it gains overkill »",
       [HEROS, *en_jeu("sv003")], ["Puzzle.Attack('sv001a')"],
       {"degats": [[VILAIN, 12]], "defausse": ["sv007", "sv003"]},
       main_exclusive=["sv007", "01088", "01090"], payer_avec=["01088", "01090"], preferer_option="Discard The Silver Surfboard"),
    _c("sv007 Cosmic Strength : option 2 contre un sbire de 3 PV, l'exces (overkill) passe au mechant",
       "12 degats sur Hydra Mercenary (3 PV) : 9 d'exces vont au vilain grace a overkill",
       [HEROS, *en_jeu("sv003"), "Puzzle.PutIntoPlay('01101')"], ["Puzzle.Attack('sv001a')"],
       {"degats": [[VILAIN, 9]], "defausse": ["sv007", "sv003"]},
       main_exclusive=["sv007", "01088", "01090"], payer_avec=["01088", "01090"], preferer_option="Discard The Silver Surfboard", cibles=["01101"]),
    _c("sv007 Cosmic Strength : option 1 contre un sbire, pas d'overkill (le vilain ne prend rien)",
       "+7 seulement : 10 degats sur Hydra Mercenary, aucun exces vers le vilain",
       [HEROS, "Puzzle.PutIntoPlay('01101')"], ["Puzzle.Attack('sv001a')"],
       {"degats": [[VILAIN, 0]], "defausse": ["sv007"]},
       main_exclusive=["sv007", "01088", "01090"], payer_avec=["01088", "01090"], preferer_option="+7 ATK", cibles=["01101"]),
    # ============================================================ sv008 Cosmic Energy
    _c("sv008 Cosmic Energy : X = 2 [energy] (Energy YY) -> 2 menaces retirees et 2 degats, et PAS de changement de forme",
       "« Remove X threat divided among schemes and deal X damage to an enemy » ; une attaque d'EVENEMENT n'est pas une attaque de base : Compunction ne part pas",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)"], [],
       {"menace": [[COMPLOT, 3]], "degats": [[VILAIN, 2]], "forme": "Hero", "defausse": ["sv008"]},
       main_exclusive=["sv008", "01088"], payer_avec=["01088"], jouer=["sv008"], cibles=[VILAIN], surpayer=True),
    _c("sv008 Cosmic Energy : paye en MENTAL (Genius BB), X = 0 -> rien ne se passe",
       "« X is the number of [energy] resources you paid » : du mental ne compte pas",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)"], [],
       {"menace": [[COMPLOT, 5]], "degats": [[VILAIN, 0]], "defausse": ["sv008"]},
       main_exclusive=["sv008", "01089"], payer_avec=["01089"], jouer=["sv008"], cibles=[VILAIN], surpayer=True),
    _c("sv008 Cosmic Energy : paiement mixte Energy YY + Genius BB, X = 2 seulement",
       "seules les ressources energie payees comptent : 2 sur 4",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)"], [],
       {"menace": [[COMPLOT, 3]], "degats": [[VILAIN, 2]], "defausse": ["sv008"]},
       main_exclusive=["sv008", "01088", "01089"], payer_avec=["01088", "01089"], jouer=["sv008"], cibles=[VILAIN], surpayer=True),
    _c("sv008 Cosmic Energy : menace repartie entre manigances (X = 2 : principale 1 -> 0 puis annexe 3 -> 2)",
       "« divided among schemes as you choose » : 2 menaces au total sur DEUX manigances (une par manigance)",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 1)", "Puzzle.Reveal('01107')"], [],
       {"menace": [[COMPLOT, 0], ["01107", 2]], "degats": [[VILAIN, 2]], "defausse": ["sv008"]},
       main_exclusive=["sv008", "01088"], payer_avec=["01088"], jouer=["sv008"], cibles=[VILAIN], surpayer=True),
    # ============================================================ sv009 Silver Up
    _c("sv009 Silver Up : retourne en Silver Surfer puis pioche 2 cartes (option 1)",
       "« Flip to Silver Surfer, then choose one: draw 2 cards... »",
       [SANS_DECK, "Puzzle.CreatePlayerDeck('01089', '01089', '01089', '01089')"], [],
       {"forme": "Hero", "taille_main": 2, "defausse": ["sv009"]},
       main_exclusive=["sv009", "01088"], payer_avec=["01088"], jouer=["sv009"], preferer_option="Draw 2 cards"),
    _c("sv009 Silver Up : retourne puis inflige 4 degats a un ennemi (option 2)",
       "« ... deal 4 damage to an enemy »",
       [], [], {"forme": "Hero", "degats": [[VILAIN, 4]], "defausse": ["sv009"]},
       main_exclusive=["sv009", "01088"], payer_avec=["01088"], jouer=["sv009"], cibles=[VILAIN],
       preferer_option="Deal 4 damage"),
    _c("sv009 Silver Up : retourne puis redresse Silver Surfer (option 3) : l'identite etait inclinee",
       "« ... or ready Silver Surfer » : le retournement PRECEDE le choix, la face heros est redressee",
       ["Puzzle.Exhaust('sv001b')"], [], {"forme": "Hero", "pret": ["sv001a"], "defausse": ["sv009"]},
       main_exclusive=["sv009", "01088"], payer_avec=["01088"], jouer=["sv009"], preferer_option="Ready Silver Surfer"),
    _c("sv009 Silver Up : avec la planche defaussee, DEUX options (pioche 2 ET 4 degats)",
       "« you may discard The Silver Surfboard, then choose two instead »",
       [*en_jeu("sv003"), SANS_DECK, "Puzzle.CreatePlayerDeck('01089', '01089', '01089', '01089')"], [],
       {"forme": "Hero", "taille_main": 2, "degats": [[VILAIN, 4]], "defausse": ["sv009", "sv003"]},
       main_exclusive=["sv009", "01088"], payer_avec=["01088"], jouer=["sv009"], cibles=[VILAIN], accepter_choix=True),
    _c("sv009 Silver Up : sans defausser la planche, UNE seule option (la planche reste en jeu)",
       "la defausse est facultative ; refusee elle laisse le choix a une option",
       [*en_jeu("sv003"), SANS_DECK, "Puzzle.CreatePlayerDeck('01089', '01089', '01089', '01089')"], [],
       {"forme": "Hero", "taille_main": 2, "degats": [[VILAIN, 0]], "en_jeu": ["sv003"]},
       main_exclusive=["sv009", "01088"], payer_avec=["01088"], jouer=["sv009"], choisir_option="Cancel"),

    # ============================================================ sv011 Silver Down
    _c("sv011 Silver Down : option 1, epuiser Norrin Radd -> l'obligation est RETIREE DE LA PARTIE",
       "« Exhaust Norrin Radd -> remove Silver Down from the game »",
       [], ["Puzzle.Reveal('sv011')"], {"exhausted": ["sv001b"], "retiree": ["sv011"]},
       main_exclusive=["01090"], verifier="sv_etat", preferer_option="Exhaust Norrin Radd"),
    _c("sv011 Silver Down : option 2, convoque Dawn Greenwood (deck) et la retire de la partie, puis l'obligation aussi",
       "« Summon Dawn Greenwood and remove her from the game -> remove Silver Down from the game »",
       [SANS_DECK, "Puzzle.CreatePlayerDeck('01090', 'sv002', '01089')"], ["Puzzle.Reveal('sv011')"],
       {"retiree": ["sv011", "sv002"], "pret": ["sv001b"], "main_ids": ["01090"], "deck_sans": ["sv002"], "retirees_n": [["sv002", 2]]},
       main_exclusive=["01090"], verifier="sv_etat", preferer_option="Summon Dawn Greenwood"),
    _c("sv011 Silver Down : Dawn dans la DEFAUSSE aussi (convocation hors deck)",
       "« summon » fouille deck, defausse, main... : Dawn defaussee est trouvee",
       [SANS_DECK, "Puzzle.CreatePlayerDeck('01090', '01089')", VIDER_DEFAUSSE, "Puzzle.CreatePlayerDiscardPile('sv002')"],
       ["Puzzle.Reveal('sv011')"], {"retiree": ["sv011"], "pret": ["sv001b"], "retirees_n": [["sv002", 2]], "defausse_sans": ["sv002"]},
       main_exclusive=["01090"], verifier="sv_etat", preferer_option="Summon Dawn Greenwood"),
    _c("sv011 Silver Down : Norrin Radd deja epuisee -> seule la convocation est possible (Dawn retiree)",
       "la 1re option exige une alter-ego prete",
       [SANS_DECK, "Puzzle.CreatePlayerDeck('01090', 'sv002')", "Puzzle.Exhaust('sv001b')"], ["Puzzle.Reveal('sv011')"],
       {"retiree": ["sv011"], "exhausted": ["sv001b"], "deck_sans": ["sv002"], "retirees_n": [["sv002", 2]]},
       main_exclusive=["01090"], verifier="sv_etat"),
    _c("sv011 Silver Down : sans Dawn hors jeu, seule l'option 1 est possible (alter-ego epuisee, Dawn intacte)",
       "la convocation n'est pas offerte quand Dawn n'existe nulle part hors jeu",
       [SANS_DECK, "Puzzle.CreatePlayerDeck('01090', '01089')"], ["Puzzle.Reveal('sv011')"],
       {"retiree": ["sv011"], "exhausted": ["sv001b"]},
       main_exclusive=["01090"], verifier="sv_etat"),
    # ============================================================ sv012 Galactus
    _c("sv012 Galactus : revele, il met The World Eater en jeu (cherche dans le deck de rencontre)",
       "« When Revealed: Reveal The World Eater and put it into play engaged with you »",
       [HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', 'sv013', '01105')"],
       ["Puzzle.Reveal('sv012')"], {"en_jeu": ["sv012", "sv013"]}, avec_boost=True, main_exclusive=["01090"]),
    _c("sv012 Galactus : vaincu, il est RETIRE DE LA PARTIE (pas defausse), sans World Eater",
       "« When Defeated: Remove Galactus from the game » : 3 degats de l'attaque de base sur 3 PV",
       [HEROS, "Puzzle.PutIntoPlay('sv012')"], ["Puzzle.Attack('sv001a')"],
       {"retiree": ["sv012"], "defausse_rencontre_sans": ["sv012"]}, main_exclusive=["01090"], cibles=["sv012"],
       verifier="sv_etat"),
    _c("sv012 Galactus : valeurs imprimees PV 3, ATK 2, SCH 2, COSMIC ELITE",
       "nombres texte <-> code (scan)", [HEROS, "Puzzle.PutIntoPlay('sv012')"], [],
       {"pv_max": [["sv012", 3]], "traits_de": [["sv012", "COSMIC"], ["sv012", "ELITE"]]}, main_exclusive=["01090"]),
    # ============================================================ sv013 The World Eater
    _c("sv013 The World Eater : Galactus ne subit aucun degat tant qu'il est en jeu",
       "« Galactus cannot take damage »",
       [HEROS, "Puzzle.PutIntoPlay('sv012')", "Puzzle.PutIntoPlay('sv013')"], ["Puzzle.Attack('sv001a')"],
       {"degats": [["sv012", 0]], "en_jeu": ["sv012", "sv013"]}, main_exclusive=["01090"], cibles=["sv012"]),
    _c("sv013 The World Eater : vaincu, il est RETIRE DE LA PARTIE (5 PV, 6 degats)",
       "« When Defeated: Remove The World Eater from the game »",
       [HEROS, "Puzzle.PutIntoPlay('sv013')", "Puzzle.Damage('sv013', 3)"], ["Puzzle.Attack('sv001a')"],
       {"retiree": ["sv013"]}, main_exclusive=["01090"], cibles=["sv013"], verifier="sv_etat"),
    _c("sv013 The World Eater : les attaques de Galactus ont overkill (exces sur l'allie vers l'identite)",
       "« his attacks gain overkill » : Galactus (ATQ 2) contre Dawn (1 PV) : 1 d'exces a l'identite, plus les 2 degats du cout de l'Interruption de Dawn (le pilote l'accepte toujours) = 3",
       [HEROS, *en_jeu("sv002"), "Puzzle.PutIntoPlay('sv012')", "Puzzle.PutIntoPlay('sv013')"],
       ["Puzzle.Defend('sv002', 'sv012')"], {"degats_identite": 3}, main_exclusive=["01090"]),
    _c("sv013 The World Eater : sans lui, Galactus n'a pas overkill (l'exces est perdu)",
       "contre-cas : sans The World Eater en jeu, l'exces est perdu : seuls les 2 degats du cout de Dawn touchent l'identite",
       [HEROS, *en_jeu("sv002"), "Puzzle.PutIntoPlay('sv012')"],
       ["Puzzle.Defend('sv002', 'sv012')"], {"degats_identite": 2}, main_exclusive=["01090"]),
    _c("sv013 The World Eater : sans World Eater, Galactus subit les degats (3 PV, 3 degats -> retire)",
       "contre-cas de l'immunite : la carte posee seule n'immunise personne",
       [HEROS, "Puzzle.PutIntoPlay('sv012')"], ["Puzzle.Attack('sv001a')"],
       {"retiree": ["sv012"]}, main_exclusive=["01090"], cibles=["sv012"], verifier="sv_etat"),
    _c("sv013 The World Eater : ne s'active pas (aucune attaque, aucune carte boost retournee)",
       "arbitrage utilisateur du 24/10/2026 : aucune valeur imprimee -> aucune activation",
       [HEROS, "Puzzle.PutIntoPlay('sv013')", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01099')"],
       ["Puzzle.Attack('sv013')"], {"degats_identite": 0, "dans_deck_rencontre": ["01099"]},
       avec_boost=True, main_exclusive=["01090"]),
    # ============================================================ sv014 The Life Stealer
    _c("sv014 The Life Stealer : revelee avec le heros seul, 2 + 1 = 3 menaces",
       "« Place 1 additional threat here for each friendly character in play » : 1 personnage ami (l'identite)",
       [HEROS], ["Puzzle.Reveal('sv014')"], {"menace": [["sv014", 3]]}, main_exclusive=["01090"]),
    _c("sv014 The Life Stealer : avec Dawn Greenwood en jeu, 2 + 2 = 4 menaces",
       "l'allie compte comme personnage ami",
       [HEROS, *en_jeu("sv002")], ["Puzzle.Reveal('sv014')"], {"menace": [["sv014", 4]]}, main_exclusive=["01090"]),
    _c("sv014 The Life Stealer : les personnages amis ont -1 ATQ (Silver Surfer : 3 -> 2 degats a Rhino)",
       "« All friendly characters get -1 ATK »",
       [HEROS, "Puzzle.Reveal('sv014')"], ["Puzzle.Attack('sv001a')"], {"degats": [[VILAIN, 2]]}, main_exclusive=["01090"]),
    # ============================================================ sv015 Cosmic Power
    _c("sv015 Cosmic Power : s'attache a Galactus quand il est en jeu",
       "« Attach to Galactus »",
       [HEROS, "Puzzle.PutIntoPlay('sv012')"], ["Puzzle.Reveal('sv015')"], {"accroche_a": [["sv015", "sv012"]]},
       main_exclusive=["01090"]),
    _c("sv015 Cosmic Power : sans Galactus, s'attache au vilain",
       "« If you cannot, attach to the villain »",
       [HEROS], ["Puzzle.Reveal('sv015')"], {"accroche_a": [["sv015", VILAIN]]}, main_exclusive=["01090"]),
    _c("sv015 Cosmic Power : les attaques du porteur gagnent overkill (Rhino contre Dawn : 1 d'exces + 2 de cout de Dawn = 3 a l'identite)",
       "« Attached enemy's attacks gain overkill »",
       [HEROS, *en_jeu("sv002"), "Puzzle.AttachReel('sv015', '01094')"], ["Puzzle.Defend('sv002', '01094')"],
       {"degats_identite": 3}, main_exclusive=["01090"]),
    _c("sv015 Cosmic Power : sans Cosmic Power, l'attaque de Rhino contre Dawn n'a pas d'overkill",
       "contre-cas : aucun exces vers l'identite (seuls les 2 degats du cout de Dawn)",
       [HEROS, *en_jeu("sv002")], ["Puzzle.Defend('sv002', '01094')"], {"degats_identite": 2}, main_exclusive=["01090"]),
    _c("sv015 Cosmic Power : Hero Action, subir 3 degats retire la carte de la partie",
       "« Hero Action: Take 3 damage -> remove Cosmic Power from the game »",
       [HEROS, "Puzzle.AttachReel('sv015', '01094')"], ["Puzzle.Action('sv015', 'HeroAction')"],
       {"degats_identite": 3, "retiree": ["sv015"]}, main_exclusive=["01090"], verifier="sv_etat"),
]

VERIFICATIONS = r'''
CLES_SV = {'retiree', 'main_ids', 'defausse_sans', 'defausse_rencontre_sans', 'deck_sans', 'retirees_n'}


def sv_etat(monde, aides):
    """etat_attendu + cles propres : retiree (card_id dans la zone « retire de la partie »), main_ids (ensemble
    exact de la main), defausse_sans (absent de la defausse du joueur), defausse_rencontre_sans (absent de la
    defausse de rencontre)."""
    from game.operate.worlds import Worlds
    cas = aides["cas"]
    attendu = dict(cas.get("attendu") or {})
    propres = {k: attendu.pop(k) for k in list(attendu) if k in CLES_SV}
    j = monde.players[0]
    soucis = []
    retirees = [getattr(f.paper, "card_id", None) for f in monde.area_removed.GetAll()]
    for cid in propres.get("retiree") or []:
        if cid not in retirees:
            soucis.append(f"{cid} n'est pas retiree de la partie (retirees = {retirees})")
    if "main_ids" in propres:
        vu = sorted(getattr(f.paper, "card_id", "?") for f in j.hand_cards.GetAll())
        if vu != sorted(propres["main_ids"]):
            soucis.append(f"main = {vu} (attendu {sorted(propres['main_ids'])})")
    for cid, n in propres.get("retirees_n") or []:
        if retirees.count(cid) != n:
            soucis.append(f"{cid} retiree {retirees.count(cid)} fois (attendu {n}) ; retirees = {retirees}")
    deck = [getattr(f.paper, "card_id", "?") for f in j.player_deck.Get(True)]
    for cid in propres.get("deck_sans") or []:
        if cid in deck:
            soucis.append(f"{cid} est encore dans le deck ({deck})")
    pile = [getattr(f.paper, "card_id", "?") for f in j.discard_pile.Get()]
    for cid in propres.get("defausse_sans") or []:
        if cid in pile:
            soucis.append(f"{cid} present dans la defausse (defausse = {pile})")
    rencontre = [getattr(f.paper, "card_id", None) for f in Worlds.GetEncounterDiscardPileCards(monde)]
    for cid in propres.get("defausse_rencontre_sans") or []:
        if cid in rencontre:
            soucis.append(f"{cid} present dans la defausse de rencontre ({rencontre})")
    sauvegarde = cas["attendu"]
    cas["attendu"] = attendu
    try:
        ok, msg = etat_attendu(monde, aides)
    finally:
        cas["attendu"] = sauvegarde
    if not ok:
        soucis.append(msg)
    if soucis:
        return False, " ; ".join(soucis)
    return True, msg
'''
