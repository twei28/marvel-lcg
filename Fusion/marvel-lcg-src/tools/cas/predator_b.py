# Cas test_capacites PREDATOR, partie 2 : sbire de joueur et cartes signature (pd003-pd008). Rappels de montage : voir predator.py.
SC = "rhino"
HEROS = "Puzzle.ChangeToFace('pd001b', 'pd001a')"
# Xenomorph's Prey (pd016, set nemesis) est EN JEU des le depart (manigance nemesis) et interdit les cartes Cloaked a Predator :
# tout cas qui pose ou mesure un Cloaked commence par la retirer.
SANS_PREY = "Puzzle.Remove('pd016')"
SANS_DECK = "Puzzle.EmptyPlayerDeck()"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01105', '01105', '01105', '01105')"]
COMPLOT = "01097b"
VILAIN = "01094"
INFRA = "pd002"
SHOCKER = "01103"   # 3 PV, sans Guard
RUNNER = "01121"    # 2 PV, sans Guard
SOLDAT = "01182"    # Hydra Soldier, 4 PV, GUARD
REINE = "pd017"


def en_jeu(*ids):
    return [f"Puzzle.PutIntoPlay('{i}', under_control=True)" for i in ids]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    if not cle.pop("avec_boost", False):
        mise = SANS_BOOST + list(mise)
    cas = {"nom": "[pd] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "predator"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "etat_attendu"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    # ============================================================ pd003 Xenomorph (sbire de joueur)
    _c("pd003 Xenomorph : joue depuis la main (cout 0), il entre en jeu ENGAGE avec son proprietaire",
       "type PlayerMinion : « when a player minion is played, it always engages its owner »",
       [HEROS], [], {"en_jeu": ["pd003"]},
       main_exclusive=["pd003"], jouer=["pd003"]),
    _c("pd003 Xenomorph : When Defeated -> Predator se redresse",
       "« When Defeated: Ready Predator »",
       [HEROS, "Puzzle.Exhaust('pd001a')", "Puzzle.PutIntoPlay('pd003')"], ["Puzzle.Damage('pd003', 9)"],
       {"pret": ["pd001a"]}, main_exclusive=["01090"]),
    _c("pd003 Xenomorph : Interrupt, vaincu il est melange dans le deck du joueur (et plus en jeu)",
       "« Interrupt: When Xenomorph is defeated, shuffle it into your deck »",
       [HEROS, "Puzzle.PutIntoPlay('pd003')", SANS_DECK, "Puzzle.CreatePlayerDeck('01089', '01089')"],
       ["Puzzle.Damage('pd003', 9)"],
       {"dans_deck_joueur": ["pd003"], "taille_deck_joueur": 3, "hors_jeu": ["pd003"]}, main_exclusive=["01090"]),
    _c("pd003 Xenomorph : Teamwork (XENOMORPH) -> avec la Reine deja en jeu, il s'active a son arrivee (Predator se defend : incline)",
       "« Teamwork (XENOMORPH) » natif : un AUTRE sbire XENOMORPH en jeu declenche une activation immediate (ATQ 2 contre DEF 2)",
       [HEROS, f"Puzzle.PutIntoPlay('{REINE}')"], [], {"exhausted": ["pd001a"]},
       main_exclusive=["pd003"], jouer=["pd003"]),
    _c("pd003 Xenomorph : SANS autre XENOMORPH en jeu, aucune activation a l'arrivee (Predator reste pret)",
       "contre-cas de Teamwork : il faut un AUTRE sbire du trait",
       [HEROS], [], {"pret": ["pd001a"]},
       main_exclusive=["pd003"], jouer=["pd003"]),
    _c("pd003 Xenomorph : valeurs imprimees PV 4, ATQ 2, MNG 0, XENOMORPH",
       "nombres texte <-> code (scan) : 0 / SCH 0 / ATK 2 / PV 4",
       [HEROS, "Puzzle.PutIntoPlay('pd003')"], [],
       {"pv_max": [["pd003", 4]], "traits_de": [["pd003", "XENOMORPH"]]},
       main_exclusive=["01090"]),
    # ============================================================ pd004 Ghost Protocol
    _c("pd004 Ghost Protocol : retire 2 menaces d'une manigance (Predator non camoufle)",
       "« Remove 2 threat from a scheme (4 threat instead if you are cloaked) »",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 6)"], [], {"menace": [[COMPLOT, 4]]},
       main_exclusive=["pd004", "01088"], jouer=["pd004"], payer_avec=["01088"], cibles=[COMPLOT]),
    _c("pd004 Ghost Protocol : Predator CAMOUFLE -> 4 menaces retirees",
       "« 4 threat instead if you are cloaked »",
       [HEROS, SANS_PREY, "Puzzle.Cloak('pd001a')", f"Puzzle.SetThreat('{COMPLOT}', 6)"], [], {"menace": [[COMPLOT, 2]]},
       main_exclusive=["pd004", "01088"], jouer=["pd004"], payer_avec=["01088"], cibles=[COMPLOT]),
    _c("pd004 Ghost Protocol : la carte Cloaked n'est PAS consommee par l'evenement (elle est seulement lue)",
       "« if you are cloaked » : condition, pas cout",
       [HEROS, SANS_PREY, "Puzzle.Cloak('pd001a')", f"Puzzle.SetThreat('{COMPLOT}', 6)"], [],
       {"statuts": [["pd001a", "Cloaked"]], "menace": [[COMPLOT, 2]]},
       main_exclusive=["pd004", "01088"], jouer=["pd004"], payer_avec=["01088"], cibles=[COMPLOT]),
    # ============================================================ pd005 Spine Rip
    _c("pd005 Spine Rip : 7 degats a un sbire de 4 PV sans Infralocked : il tombe, l'exces ne va PAS au vilain",
       "« Deal 7 damage to an enemy »",
       ["Puzzle.PutIntoPlay('01182')", HEROS], [], {"degats": [[VILAIN, 0]], "hors_jeu": ["01182"]},
       main_exclusive=["pd005", "01090", "01088"], jouer=["pd005"], payer_avec=["01090", "01088"], cibles=["01182"]),
    _c("pd005 Spine Rip : Infralocked sur la cible -> overkill, l'exces (7 - 2 PV = 5) frappe le vilain",
       "« If that enemy has Infralocked attached, this attack gains overkill »",
       [HEROS, f"Puzzle.PutIntoPlay('{RUNNER}')"], [], {"degats": [[VILAIN, 5]], "hors_jeu": [RUNNER]},
       main_exclusive=["pd005", "01090", "01088"], jouer=["pd005"], payer_avec=["01090", "01088"], cibles=[RUNNER]),
    _c("pd005 Spine Rip : sans Infralocked sur la cible -> PAS d'overkill, le vilain ne prend rien",
       "contre-cas : l'overkill est conditionnel",
       [HEROS, f"Puzzle.PutIntoPlay('{RUNNER}')", f"Puzzle.PutIntoPlay('{SHOCKER}')"], [],
       {"degats": [[VILAIN, 0]], "hors_jeu": [RUNNER]},
       main_exclusive=["pd005", "01090", "01088"], jouer=["pd005"], payer_avec=["01090", "01088"], cibles=[RUNNER]),
    # ============================================================ pd006 Shadow Counter
    _c("pd006 Shadow Counter : attaque de Sandman (ATQ 3 - DEF 2 = 1 degat) -> tout est evite et Predator est camoufle",
       "« prevent 3 of that damage. Then, give Predator a cloaked status card »",
       [HEROS, SANS_PREY, "Puzzle.PutIntoPlay('01102')"], ["Puzzle.Attack('01102')"],
       {"degats_identite": 0, "statuts": [["pd001a", "Cloaked"]]},
       main_exclusive=["pd006", "01089"], payer_avec=["01089"]),
    _c("pd006 Shadow Counter : 5 degats directs -> 3 evites, 2 subis, puis camoufle (n'est PAS limite aux attaques)",
       "« When you would take ANY amount of damage » : aucun is_from_attack",
       [HEROS, SANS_PREY], ["Puzzle.Damage('pd001a', 5)"],
       {"degats_identite": 2, "statuts": [["pd001a", "Cloaked"]]},
       main_exclusive=["pd006", "01089"], payer_avec=["01089"]),
    # ============================================================ pd007 Savage Skewer
    _c("pd007 Savage Skewer : 5 degats au vilain ; Predator NON camoufle -> aucune option, aucun statut",
       "« You MAY discard a cloaked status card to... » : sans carte Cloaked, rien n'est offert",
       [HEROS, SANS_PREY, "Puzzle.PutIntoPlay('01100')"], [],
       {"degats": [[VILAIN, 5]], "statuts_absents": [[VILAIN, "Stunned"], [VILAIN, "Confused"]],
        "attaches": [[VILAIN, "01100"]]},
       main_exclusive=["pd007", "01090"], jouer=["pd007"], payer_avec=["01090"], cibles=[VILAIN]),
    _c("pd007 Savage Skewer : camoufle, branche « stun and confuse » -> le vilain est etourdi ET desoriente, Cloaked defaussee",
       "« discard a cloaked status card to either stun and confuse that enemy »",
       [HEROS, SANS_PREY, "Puzzle.Cloak('pd001a')"], [],
       {"degats": [[VILAIN, 5]], "statuts": [[VILAIN, "Stunned"], [VILAIN, "Confused"]],
        "statuts_absents": [["pd001a", "Cloaked"]]},
       main_exclusive=["pd007", "01090"], jouer=["pd007"], payer_avec=["01090"], cibles=[VILAIN],
       preferer_option="stun and confuse"),
    _c("pd007 Savage Skewer : camoufle, branche « attachement » -> l'attachement a Hero Action est defausse, pas d'etourdissement",
       "« or discard an attachment on that enemy with the text Hero Action or Hero Response » (01100 Enhanced Ivory Horn)",
       [HEROS, SANS_PREY, "Puzzle.Cloak('pd001a')", "Puzzle.PutIntoPlay('01100')"], [],
       {"degats": [[VILAIN, 5]], "statuts_absents": [[VILAIN, "Stunned"], [VILAIN, "Confused"], ["pd001a", "Cloaked"]],
        "defausse_rencontre": ["01100"]},
       main_exclusive=["pd007", "01090"], jouer=["pd007"], payer_avec=["01090"], cibles=[VILAIN],
       preferer_option="attachment"),
    _c("pd007 Savage Skewer : camoufle mais le joueur REFUSE (Cancel) -> Cloaked conservee, rien d'autre",
       "« You MAY » : le refus ne coute rien",
       [HEROS, SANS_PREY, "Puzzle.Cloak('pd001a')"], [],
       {"degats": [[VILAIN, 5]], "statuts": [["pd001a", "Cloaked"]],
        "statuts_absents": [[VILAIN, "Stunned"], [VILAIN, "Confused"]]},
       main_exclusive=["pd007", "01090"], jouer=["pd007"], payer_avec=["01090"], cibles=[VILAIN],
       choisir_option="Cancel"),
    # ============================================================ pd008 Jungle Stalk
    _c("pd008 Jungle Stalk : trouve un sbire a 2 icones de boost (Shocker) -> 2 PV soignes, Predator camoufle, sbire engage",
       "« Find a minion ... engaged with you -> heal damage for each icon in that card's boost area and give Predator a cloaked status card »",
       [HEROS, SANS_PREY, "Puzzle.Damage('pd001a', 5)", "Puzzle.EmptyEncounterDeck()",
        f"Puzzle.CreateEncounterDeck('{SHOCKER}', '01105', '01105', '01105')"], [],
       {"degats_identite": 3, "statuts": [["pd001a", "Cloaked"]], "en_jeu": [SHOCKER]},
       main_exclusive=["pd008"], jouer=["pd008"], avec_boost=True),
    _c("pd008 Jungle Stalk : sbire a ETOILE seulement (Weapons Runner : 0 icone + l'etoile) -> 1 PV soigne",
       "« each icon (STAR and Y) » : l'icone a etoile compte comme une icone",
       [HEROS, SANS_PREY, "Puzzle.Damage('pd001a', 5)", "Puzzle.EmptyEncounterDeck()",
        f"Puzzle.CreateEncounterDeck('{RUNNER}', '01105', '01105', '01105')"], [],
       {"degats_identite": 4, "statuts": [["pd001a", "Cloaked"]], "en_jeu": [RUNNER]},
       main_exclusive=["pd008"], jouer=["pd008"], avec_boost=True),
    _c("pd008 Jungle Stalk : Drone (1 icone + etoile) -> 2 PV soignes (etoile ET icone comptees)",
       "« each icon (STAR and Y) » : 1 icone ordinaire + l'etoile = 2",
       [HEROS, SANS_PREY, "Puzzle.Damage('pd001a', 5)", "Puzzle.EmptyEncounterDeck()",
        "Puzzle.CreateEncounterDeck('pd018', '01105', '01105', '01105')"], [],
       {"degats_identite": 3, "en_jeu": ["pd018"]},
       main_exclusive=["pd008"], jouer=["pd008"], avec_boost=True),
    _c("pd008 Jungle Stalk : AUCUN sbire a trouver -> rien (ni soin, ni Cloaked) : « Find » est un COUT",
       "la fleche : trouver est le cout, sans sbire la carte n'a aucun effet",
       [HEROS, SANS_PREY, "Puzzle.Damage('pd001a', 5)", "Puzzle.EmptyEncounterDeck()", "Puzzle.EmptyEncounterDiscardPile()",
        "Puzzle.RemoveNemesisAside()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105')", SANS_DECK], [],
       {"degats_identite": 5, "statuts_absents": [["pd001a", "Cloaked"]]},
       main_exclusive=["pd008"], jouer=["pd008"], avec_boost=True),
    _c("pd008 Jungle Stalk : « Find » balaie TOUTES les zones, y compris le deck du joueur : son propre Xenomorph (sbire de joueur) est trouve",
       "regle Find (game/operate/find.py) : player deck compris ; pd003 est un SBIRE de joueur, donc un candidat (cout 0 : 0 icone, aucun soin)",
       [HEROS, SANS_PREY, "Puzzle.Damage('pd001a', 5)", "Puzzle.EmptyEncounterDeck()", "Puzzle.EmptyEncounterDiscardPile()",
        "Puzzle.RemoveNemesisAside()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105')", SANS_DECK,
        "Puzzle.CreatePlayerDeck('pd003', '01089')"], [],
       {"degats_identite": 5, "statuts": [["pd001a", "Cloaked"]], "en_jeu": ["pd003"]},
       main_exclusive=["pd008"], jouer=["pd008"], avec_boost=True),
]
