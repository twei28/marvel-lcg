# Cas test_capacites des cartes de RENCONTRE du scenario 1 « The Big Apple » (pu007-pu022), PU-7. Prefixe `[renc]`.
# Montage : scenario `rhino` (Rhino = « le vilain » hors ville), Spider-Man ; la ville reelle (9 lieux) pour les cartes qui lisent la position.
# `main_exclusive` evite Great Responsibility (01061), que le pilote jouerait pour annuler une menace.
FORME_HEROS = "Puzzle.ChangeForm('01001b')"
SANS_DEFENSE = {"passer_sur_option": "Defense"}
GRILLE_REELLE = [["pu030", "pu031", "pu032"], ["pu033", "pu034", "pu035"], ["pu036", "pu037", "pu038"]]
G = repr(GRILLE_REELLE)
CASE = {"pu030": (0, 0), "pu031": (0, 1), "pu032": (0, 2), "pu033": (1, 0), "pu034": (1, 1), "pu035": (1, 2), "pu036": (2, 0), "pu037": (2, 1), "pu038": (2, 2)}


def ville(lieu="pu034", communs=("pu005", "pu006")):
    return [*["Puzzle.PutIntoPlay('%s')" % x for x in communs],
            "Puzzle.InstallerVille(%s, %s, en_jeu=True)" % (G, repr(CASE[lieu])),
            *["Puzzle.MoveCardToGameArea('%s', 1)" % x for x in communs]]


def _r(nom, pourquoi, mise, declencher, attendu, deck=("01105", "01105", "01105"), heros=True, verifier="big_etat", **cle):
    cas = {"nom": "[renc] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", "rhino"), "heros": "spider_man",
           "mise_en_place": ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck(%s)" % ", ".join(repr(x) for x in deck),
                             *([FORME_HEROS] if heros else []), *mise],
           "declencher": declencher, "verifier": verifier, "attendu": attendu, "main_exclusive": ["01088"]}
    cas.update(cle)
    return cas


CAS = [
    # ------------------------------------------------------------------------------------------------ pu017 Conflicting Evidence
    _r("pu017 Conflicting Evidence (Alter-Ego) : le vilain attaque SANS carte de boost -> 2 degats (ATQ 2 de Rhino), pas 4 malgre le Shocker au dessus du deck",
       "« The villain attacks you. Do not give them a boost card for this attack »", [], ["Puzzle.Reveal('pu017')"], {"degats_identite": 2},
       deck=("01105", "01103"), heros=False),
    _r("pu017 Conflicting Evidence (Hero) : le vilain manigance SANS carte de boost -> 1 menace (SCH 1), pas 3", "« The villain schemes. Do not give them a boost card »",
       ["Puzzle.SetThreat('01097b', 0)"], ["Puzzle.Reveal('pu017')"], {"menace": [["01097b", 1]]}, deck=("01105", "01103")),
    # ------------------------------------------------------------------------------------------------ pu021 Bank Robbery
    _r("pu021 Bank Robbery : chaque joueur glisse UNE carte au hasard de sa main sous la manigance (2 joueurs : 2 cartes)", "When Revealed ; « each player »",
       ["Puzzle.CreateHandCards('01089')"], ["Puzzle.Reveal('pu021')"], {"taille_pose_sous": [["pu021", 2]]}, heros2="spider_man", main_exclusive=["01088", "01089"],
       verifier="etat_attendu"),
    _r("pu021 Bank Robbery : la manigance est vaincue -> les cartes glissees reviennent en main de leur proprietaire (main de 2)", "When Defeated",
       [], ["Puzzle.Reveal('pu021')", "Puzzle.SetThreat('pu021', 0)"], {"taille_main": 2},
       main_exclusive=["01088", "01089"], verifier="etat_attendu"),
    # ------------------------------------------------------------------------------------------------ pu009 Hunted by the Past
    _r("pu009 Hunted by the Past : trouve MON sbire nemesis (Vulture 01167), le revele, s'y attache ; le sbire gagne +3 PV (4 -> 7)",
       "When Revealed ; « Attached minion gets +3 hit points »", [], ["Puzzle.Reveal('pu009')"],
       {"hotes": [["pu009", "01167"]], "pv_max": [["01167", 7]]}, deck=("01105", "01167"), verifier="etat_attendu"),
    # ------------------------------------------------------------------------------------------------ pu011 Bellona
    _r("pu011 Bellona : ses attaques PERCENT -> contre un heros Tough, la carte Tough est defaussee ET le degat passe (1)",
       "« Bellona's attacks gain piercing »", ["Puzzle.PutIntoPlay('pu011')", "Puzzle.Tough('01001a')"],
       ["Puzzle.EnemyAttacks('pu011', '01001a')"], {"degats_identite": 1, "statuts_absents": [["01001a", "Tough"]]}, **SANS_DEFENSE, verifier="etat_attendu"),
    _r("pu011 TEMOIN : un sbire sans perforation (Hydra Mercenary ATQ 1) contre un heros Tough -> la carte Tough absorbe, 0 degat", "temoin de piercing",
       ["Puzzle.PutIntoPlay('01101')", "Puzzle.Tough('01001a')"], ["Puzzle.EnemyAttacks('01101', '01001a')"], {"degats_identite": 0, "statuts_absents": [["01001a", "Tough"]]},
       **SANS_DEFENSE, verifier="etat_attendu"),
    _r("pu011 Bellona vaincue PAR UNE ATTAQUE du joueur, qui REFUSE de prendre 2 degats -> elle est melangee dans le deck de rencontre, 0 degat",
       "When Defeated ; « may take 2 damage » : refus = « Cancel » ; la 1re vague de degats est absorbee par sa carte Tough",
       ["Puzzle.PutIntoPlay('pu011')", "Puzzle.Damage('pu011', 1)", "Puzzle.Damage('pu011', 4)"], ["Puzzle.Attack('01001a')"],
       {"dans_deck_rencontre": ["pu011"], "degats_identite": 0}, choisir_option=["Cancel"], cibles=["pu011"], verifier="etat_attendu"),
    _r("pu011 Bellona vaincue PAR UNE ATTAQUE du joueur, qui ACCEPTE -> il prend 2 degats et elle va en DEFAUSSE de rencontre",
       "« may take 2 damage to discard her instead »",
       ["Puzzle.PutIntoPlay('pu011')", "Puzzle.Damage('pu011', 1)", "Puzzle.Damage('pu011', 4)"], ["Puzzle.Attack('01001a')"],
       {"defausse_rencontre": ["pu011"], "degats_identite": 2}, cibles=["pu011"], verifier="etat_attendu"),
    _r("pu011 Bellona vaincue SANS joueur vainqueur (degats d'un effet) -> melangee d'office, 0 degat", "pas de joueur vainqueur : pas de choix",
       ["Puzzle.PutIntoPlay('pu011')"], ["Puzzle.Damage('pu011', 1)", "Puzzle.Damage('pu011', 5)"], {"dans_deck_rencontre": ["pu011"], "degats_identite": 0},
       verifier="etat_attendu"),
    # ------------------------------------------------------------------------------------------------ pu012 Black Tarantula
    _r("pu012 Black Tarantula : 2 pistes en victoire (1 joueur : palier 2) -> +3 PV (4 -> 7)", "paliers cumules : « at least 2[per hero] »",
       ["Puzzle.PutIntoPlay('pu012')"], ["Puzzle.AddToVictoryDisplay('pu041')", "Puzzle.AddToVictoryDisplay('pu042')"], {"pv_max": [["pu012", 7]], "quickstrike": [["pu012", True]]}, verifier="renc_etat"),
    _r("pu012 Black Tarantula, TEMOIN : 1 piste en victoire -> PV inchanges (4)", "palier 1 : quickstrike seulement", ["Puzzle.PutIntoPlay('pu012')"],
       ["Puzzle.AddToVictoryDisplay('pu041')"], {"pv_max": [["pu012", 4]], "quickstrike": [["pu012", True]]}, verifier="renc_etat"),
    _r("pu012 Black Tarantula, TEMOIN : AUCUNE piste en victoire -> ni quickstrike ni PV en plus", "sous le palier 1", ["Puzzle.PutIntoPlay('pu012')"], [],
       {"pv_max": [["pu012", 4]], "quickstrike": [["pu012", False]]}, verifier="renc_etat"),
    # ------------------------------------------------------------------------------------------------ pu016 Busted!
    _r("pu016 Busted! : un sbire est vaincu a Hell's Kitchen alors que la piste est en jeu -> AUCUN compteur (on ne declenche pas les capacites des pistes)",
       "« You cannot ... trigger abilities on LEAD cards »",
       ["Puzzle.PutIntoPlay('01103')", *ville("pu030"), "Puzzle.PutIntoPlay('pu039', under_control=True)", "Puzzle.PutIntoPlay('pu016', under_control=True)"],
       ["Puzzle.Damage('01103', 3)"], {"compteurs": [["pu039", "bouncer", 0]]}),
    _r("pu016 Busted!, TEMOIN : meme situation SANS Busted! -> 1 compteur", "ligne de base : sans la condition, la piste compte",
       ["Puzzle.PutIntoPlay('01103')", *ville("pu030"), "Puzzle.PutIntoPlay('pu039', under_control=True)"],
       ["Puzzle.Damage('01103', 3)"], {"compteurs": [["pu039", "bouncer", 1]]}),
    _r("pu016 Busted! : le heros ne peut PAS attaquer le vilain (CAPO de sa zone) -> 0 degat", "« You cannot attack the villain »",
       [*ville("pu030"), "Puzzle.PutIntoPlay('pu055a')", "Puzzle.MoveCardToGameArea('pu055a', 2)", "Puzzle.PutIntoPlay('pu016', under_control=True)"],
       ["Puzzle.Attack('01001a')"], {"degats": [["pu055a", 0]]}, cibles=["pu055a"]),
    _r("pu016 Busted!, TEMOIN : meme attaque sans Busted! -> 2 degats", "ligne de base",
       [*ville("pu030"), "Puzzle.PutIntoPlay('pu055a')", "Puzzle.MoveCardToGameArea('pu055a', 2)"],
       ["Puzzle.Attack('01001a')"], {"degats": [["pu055a", 2]]}, cibles=["pu055a"]),
    _r("pu016 Busted! (Alter-Ego Action) : epuiser l'identite et defausser une carte -> la condition est defaussee", "cout = epuiser + defausser ; effet = se defausser",
       ["Puzzle.PutIntoPlay('pu016', under_control=True)"], ["Puzzle.Action('pu016', 'AlterEgoAction')"],
       {"hors_jeu": ["pu016"], "exhausted": ["01001b"], "defausse": ["01088"]}, heros=False, verifier="etat_attendu"),
    # ------------------------------------------------------------------------------------------------ pu018 Red Herring
    _r("pu018 Red Herring : la piste de Midtown est dans mon aire -> je vais au premier lieu choisi (Hell's Kitchen (0,0), le choix par defaut) et mon identite est etourdie",
       "When Revealed ; « Move to a location not mentioned on the LEAD card » ; « stun or confuse »",
       [*ville("pu034"), "Puzzle.PutIntoPlay('pu043', under_control=True)"], ["Puzzle.Reveal('pu018')"],
       {"case_de": [[0, [0, 0]]], "zone_de": [["01001a", 2]], "statuts": [["01001a", "Stunned"]]}),
    _r("pu018 Red Herring : la piste de Hell's Kitchen est dans mon aire -> Hell's Kitchen est EXCLU, je vais a Theater District (0,1)",
       "« not mentioned on the LEAD card »", [*ville("pu034"), "Puzzle.PutIntoPlay('pu039', under_control=True)"], ["Puzzle.Reveal('pu018')"],
       {"case_de": [[0, [0, 1]]], "zone_de": [["01001a", 2]]}),
    _r("pu018 Red Herring : je choisis de rendre mon identite CONFUSE (et non etourdie)", "« stun OR confuse »",
       [*ville("pu034"), "Puzzle.PutIntoPlay('pu043', under_control=True)"], ["Puzzle.Reveal('pu018')"],
       {"statuts": [["01001a", "Confused"]], "statuts_absents": [["01001a", "Stunned"]]}, preferer_option="Confuse"),
    # ------------------------------------------------------------------------------------------------ pu020 Shootout
    _r("pu020 Shootout : 1 degat au CAPO de ma zone, a moi, a mon allie et a un sbire de ma zone ; PAS a Rhino (autre zone)",
       "When Revealed ; « the villain and each character in this turf »",
       ["Puzzle.PutIntoPlay('01075', under_control=True)", "Puzzle.PutIntoPlay('01103')", *ville("pu034"), "Puzzle.PutIntoPlay('pu055a')",
        "Puzzle.MoveCardToGameArea('pu055a', 3)"], ["Puzzle.Reveal('pu020')"],
       {"degats": [["pu055a", 1], ["01075", 1], ["01103", 1], ["01094", 0]], "degats_identite": 1}),
    _r("pu020 Shootout (Boost) : le boost inflige 1 degat a chaque personnage que je controle (mon allie en subit 1)", "★ Boost",
       ["Puzzle.PutIntoPlay('01075', under_control=True)"], ["Puzzle.Boost('pu020')"],
       {"degats": [["01075", 1]]}, verifier="etat_attendu"),
]


VERIFICATIONS = r'''
def renc_etat(monde, aides):
    """Cle propre : `quickstrike` [[card_id, bool]] ; le reste va a `big_etat`."""
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    soucis = []
    for card_id, voulu in attendu.get("quickstrike") or []:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable")
        elif bool(face.IsQuickstrike()) != voulu:
            soucis.append(f"{card_id} quickstrike = {face.IsQuickstrike()} (attendu {voulu})")
    cas["attendu"] = {k: v for k, v in attendu.items() if k != "quickstrike"}
    try:
        if cas["attendu"]:
            ok, msg = big_etat(monde, aides)
            if not ok:
                soucis.append(msg)
    finally:
        cas["attendu"] = attendu
    return (False, " ; ".join(soucis)) if soucis else (True, "carte de rencontre conforme")
'''
