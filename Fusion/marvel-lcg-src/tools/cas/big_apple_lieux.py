# Cas test_capacites des cartes LIEES AUX LIEUX du scenario 1 « The Big Apple » (pu007 pu008 pu010 pu013 pu014 pu015 pu022), PU-7 M5. Prefixe `[lieu]`.
# Montage : scenario `rhino`, Spider-Man en forme heros, la ville reelle (9 lieux, depart Midtown (1,1)). Un sbire « attache » est GLISSE sous la carte
# de lieu (`Ville.AttacherSbire`) : hors jeu, mais ses Interruptions « entre dans son lieu » restent actives (`NoOutOfPlayLimit`).
# ⚠ `Puzzle.CreateEncounterDeck(a, b, c)` : le DESSUS du deck est le DERNIER argument.
FORME_HEROS = "Puzzle.ChangeForm('01001b')"
SANS_DEFENSE = {"passer_sur_option": "Defense"}
GRILLE_REELLE = [["pu030", "pu031", "pu032"], ["pu033", "pu034", "pu035"], ["pu036", "pu037", "pu038"]]
G = repr(GRILLE_REELLE)
MAIN = ["01088", "01089", "01090"]


def ville(lieu=(1, 1), communs=("pu005", "pu006")):
    return [*["Puzzle.PutIntoPlay('%s')" % x for x in communs],
            "Puzzle.InstallerVille(%s, %s, en_jeu=True)" % (G, repr(tuple(lieu))),
            *["Puzzle.MoveCardToGameArea('%s', 1)" % x for x in communs]]


def _l(nom, pourquoi, mise, declencher, attendu, deck=("01105", "01105", "01105"), **cle):
    cas = {"nom": "[lieu] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", "rhino"), "heros": "spider_man",
           "mise_en_place": ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck(%s)" % ", ".join(repr(x) for x in deck),
                             FORME_HEROS, *mise],
           "declencher": declencher, "verifier": "lieu_etat", "attendu": attendu, "main_exclusive": ["01088"]}
    cas.update(cle)
    return cas


CAS = [
    # ------------------------------------------------------------------------------------------------ pu007 Burning Building
    _l("pu007 Burning Building (When Revealed) : s'attache a un lieu INOCCUPE (le 1er : Hell's Kitchen) et y pose 1 jeton d'acceleration",
       "« Attach to an unoccupied location and place 1 acceleration token here »", [*ville()], ["Puzzle.Reveal('pu007')"],
       {"hotes": [["pu007", "pu030"]], "compteurs": [["pu007", "acceleration", 1]]}),
    _l("pu007 Burning Building : un lieu OCCUPE est exclu (le 2e joueur est a Hell's Kitchen) -> Theater District",
       "« unoccupied » = sans aucun joueur", [*ville()], ["Puzzle.PlacerDansLaVille((0, 0), 1)", "Puzzle.Reveal('pu007')"],
       {"hotes": [["pu007", "pu031"]]}, heros2="spider_man"),
    _l("pu007 Burning Building : plus de ville (aucun lieu) -> surge (la carte suivante est revelee) et la carte est defaussee",
       "« Otherwise, surge »", [], ["Puzzle.Reveal('pu007')"], {"defausse_rencontre": ["pu007"], "carte_du_surge": "01103"}, deck=("01105", "01105", "01103")),
    _l("pu007 Burning Building (Forced Response) : la phase des joueurs se termine -> un 2e jeton", "« After the player phase ends, place 1 acceleration token »",
       [*ville()], ["Puzzle.Reveal('pu007')", "Puzzle.EndPlayerPhase()"], {"compteurs": [["pu007", "acceleration", 2]]}),
    _l("pu007 Burning Building (Hero Action) : 2 jetons, le joueur est au lieu -> identite epuisee, 2 cartes defaussees du deck (31 -> 29), la carte est defaussee",
       "cout = epuiser l'identite ; effet = defausser autant de cartes que de jetons, puis se defausser",
       [*ville()], ["Puzzle.Reveal('pu007')", "Puzzle.PlacerDansLaVille((0, 0))", "Puzzle.EndPlayerPhase()", "Puzzle.Action('pu007', 'HeroAction')"],
       {"hors_jeu": ["pu007"], "exhausted": ["01001a"], "taille_deck_joueur": 29}, main_exclusive=MAIN),
    _l("pu007 Burning Building, TEMOIN : le joueur n'est PAS au lieu porteur (Midtown) -> l'Action n'est pas offerte (deck et identite intacts)",
       "R3 : on n'interagit qu'avec le lieu qu'on occupe", [*ville()], ["Puzzle.Reveal('pu007')", "Puzzle.EndPlayerPhase()"],
       {"en_jeu": ["pu007"], "pret": ["01001a"], "taille_deck_joueur": 31}, main_exclusive=MAIN,
       declencher_tolerant=["Puzzle.Action('pu007', 'HeroAction')"]),
    # ------------------------------------------------------------------------------------------------ pu008 Citizens in Danger!
    _l("pu008 Citizens in Danger! (When Revealed) : le joueur epuise son identite et la carte s'attache a SON lieu (Midtown)",
       "« Exhaust your identity. Attach this card to your current location »", [*ville()], ["Puzzle.Reveal('pu008')"],
       {"hotes": [["pu008", "pu034"]], "exhausted": ["01001a"]}),
    _l("pu008 Citizens in Danger! : plus de ville -> identite epuisee quand meme, surge, carte defaussee", "« if you cannot, surge »", [], ["Puzzle.Reveal('pu008')"],
       {"exhausted": ["01001a"], "defausse_rencontre": ["pu008"], "carte_du_surge": "01103"}, deck=("01105", "01105", "01103")),
    _l("pu008 Citizens in Danger! (Forced Interrupt) : le joueur QUITTE le lieu -> une carte de rencontre lui est distribuee face cachee (1) et la carte est defaussee",
       "« When a player leaves this location, deal them a facedown encounter card and discard this card »",
       [*ville()], ["Puzzle.Reveal('pu008')", "Puzzle.DeplacerDansLaVille((0, 1))"],
       {"distribuees": [[0, 1]], "defausse_rencontre": ["pu008"], "case_de": [[0, [0, 1]]]}, deck=("01105", "01105")),
    _l("pu008 Citizens in Danger!, TEMOIN : un AUTRE lieu que le porteur est quitte (le 2e joueur part de Hell's Kitchen) -> rien (la carte reste attachee)",
       "« this location » seulement", [*ville()],
       ["Puzzle.PlacerDansLaVille((0, 0), 1)", "Puzzle.Reveal('pu008')", "Puzzle.DeplacerDansLaVille((0, 1), 1)"],
       {"hotes": [["pu008", "pu034"]], "distribuees": [[1, 0]]}, heros2="spider_man"),
    # ------------------------------------------------------------------------------------------------ pu010 "It's a Trap!"
    _l("pu010 \"It's a Trap!\" (When Revealed) : s'attache au lieu actuel (Midtown)", "« Attach to your current location »", [*ville()], ["Puzzle.Reveal('pu010')"],
       {"hotes": [["pu010", "pu034"]]}),
    _l("pu010 \"It's a Trap!\" : plus de ville -> surge, carte defaussee", "« if you cannot, surge »", [], ["Puzzle.Reveal('pu010')"],
       {"defausse_rencontre": ["pu010"], "carte_du_surge": "01103"}, deck=("01105", "01105", "01103")),
    _l("pu010 \"It's a Trap!\" (QUITTE le lieu) : le joueur trouve un sbire (Shocker), le revele (il s'engage avec lui) ; chaque sbire engage s'active (ATQ 2 + 1 de boost : 3 degats) ; la carte est defaussee",
       "« When a player enters or leaves this location, they find a minion not in play and reveal it. Each minion engaged with that player activates. Then, discard »",
       [*ville()], ["Puzzle.Reveal('pu010')", "Puzzle.DeplacerDansLaVille((0, 1))"],
       {"engage": [["01103", 0]], "degats_identite": 3, "defausse_rencontre": ["pu010"]}, deck=("01103", "01105"), **SANS_DEFENSE),
    _l("pu010 \"It's a Trap!\" (ENTRE dans le lieu) : le 2e joueur arrive a Midtown -> c'est LUI qui trouve le sbire, qui s'engage avec lui",
       "« enters » : meme effet, joueur qui entre", [*ville()],
       ["Puzzle.PlacerDansLaVille((0, 0), 1)", "Puzzle.Reveal('pu010')", "Puzzle.PlacerDansLaVille((1, 1), 1)"],
       {"engage": [["01103", 1]], "defausse_rencontre": ["pu010"]}, deck=("01103", "01105"), heros2="spider_man"),
    _l("pu010 \"It's a Trap!\", TEMOIN : le joueur se deplace entre deux AUTRES lieux -> rien (pas de sbire, la carte reste)", "« this location » seulement",
       [*ville()], ["Puzzle.PlacerDansLaVille((0, 0), 1)", "Puzzle.Reveal('pu010')", "Puzzle.DeplacerDansLaVille((0, 1), 1)"],
       {"hotes": [["pu010", "pu034"]], "engage": [["01103", None]]}, deck=("01105", "01103"), heros2="spider_man"),
    # ------------------------------------------------------------------------------------------------ pu013 Overdrive
    _l("pu013 Overdrive (Forced Response) : fin du round -> il s'attache a un lieu inoccupe (Hell's Kitchen) et n'est plus engage",
       "« After the round ends, attach Overdrive to an unoccupied location »", [*ville(), "Puzzle.PutIntoPlay('pu013')"], ["Puzzle.SendAfterRoundEnd()"],
       {"attache_a": [["pu013", "pu030"]], "engage": [["pu013", None]]}),
    _l("pu013 Overdrive : un lieu OCCUPE est exclu (2e joueur a Hell's Kitchen) -> Theater District", "« unoccupied »",
       [*ville(), "Puzzle.PutIntoPlay('pu013')"], ["Puzzle.PlacerDansLaVille((0, 0), 1)", "Puzzle.SendAfterRoundEnd()"],
       {"attache_a": [["pu013", "pu031"]]}, heros2="spider_man"),
    _l("pu013 Overdrive : aucun lieu (plus de ville) -> « if able » : il reste engage", "« if able »",
       ["Puzzle.PutIntoPlay('pu013')"], ["Puzzle.SendAfterRoundEnd()"], {"engage": [["pu013", 0]]}),
    _l("pu013 Overdrive (Forced Interrupt) : le joueur ENTRE dans son lieu (Theater District) -> il s'engage avec lui, et son Quickstrike l'attaque UNE fois (2 degats, plus les 2 de sa mise en jeu : 4)",
       "« When a player enters Overdrive's location, he engages them » ; Quickstrike a l'engagement",
       [*ville(), "Puzzle.PutIntoPlay('pu013')", "Puzzle.AttacherAuLieu('pu013', 'pu031')"], ["Puzzle.DeplacerDansLaVille((0, 1))"],
       {"engage": [["pu013", 0]], "attache_a": [["pu013", None]], "degats_identite": 4}, **SANS_DEFENSE),
    _l("pu013 Overdrive, TEMOIN DE BASE : mis en jeu normalement (engage d'office), son Quickstrike frappe UNE fois", "ligne de base de l'attaque",
       [*ville()], ["Puzzle.PutIntoPlay('pu013')"], {"engage": [["pu013", 0]], "degats_identite": 2}, **SANS_DEFENSE),
    _l("pu013 Overdrive, TEMOIN : le joueur va ailleurs (Lower East Side) -> il reste attache et n'attaque pas", "l'Interruption ne part que pour SON lieu",
       [*ville(), "Puzzle.PutIntoPlay('pu013')", "Puzzle.AttacherAuLieu('pu013', 'pu031')"], ["Puzzle.DeplacerDansLaVille((1, 2))"],
       {"engage": [["pu013", None]], "attache_a": [["pu013", "pu031"]], "degats_identite": 0}),
    _l("pu013 Overdrive : etourdi (Stunned) puis attache puis engage de nouveau -> il garde son statut", "« He remains in play » : ses cartes de statut restent",
       [*ville(), "Puzzle.PutIntoPlay('pu013')", "Puzzle.Stun('pu013')", "Puzzle.AttacherAuLieu('pu013', 'pu031')"], ["Puzzle.DeplacerDansLaVille((0, 1))"],
       {"engage": [["pu013", 0]], "statuts": [["pu013", "Stunned"]]}, **SANS_DEFENSE),
    _l("pu013 Overdrive : TENACE (Tough) puis attache puis engage de nouveau -> il garde sa carte Tenace", "« He remains in play » : ses cartes de statut restent",
       [*ville(), "Puzzle.PutIntoPlay('pu013')", "Puzzle.Tough('pu013')", "Puzzle.AttacherAuLieu('pu013', 'pu031')"], ["Puzzle.DeplacerDansLaVille((0, 1))"],
       {"engage": [["pu013", 0]], "statuts": [["pu013", "Tough"]]}, **SANS_DEFENSE),
    _l("pu013 Overdrive : blesse (1 degat) puis attache puis engage de nouveau -> il garde ses degats (2 PV sur 3)", "« He remains in play » : ses degats restent",
       [*ville(), "Puzzle.PutIntoPlay('pu013')", "Puzzle.Damage('pu013', 1)", "Puzzle.AttacherAuLieu('pu013', 'pu031')"], ["Puzzle.DeplacerDansLaVille((0, 1))"],
       {"engage": [["pu013", 0]], "pv_de": [["pu013", 2]]}, **SANS_DEFENSE),
    # ------------------------------------------------------------------------------------------------ pu014 Muse
    _l("pu014 Muse (Forced Response) : apres qu'il s'est active (attaque, ATQ 2 : 2 degats) -> il s'attache a un lieu inoccupe (Hell's Kitchen)",
       "« After Muse activates, attach him to an unoccupied location »", [*ville(), "Puzzle.PutIntoPlay('pu014')"], ["Puzzle.EnemyAttacks('pu014', '01001a')"],
       {"attache_a": [["pu014", "pu030"]], "engage": [["pu014", None]], "degats_identite": 2}, **SANS_DEFENSE),
    _l("pu014 Muse : aucun lieu (plus de ville) -> il reste engage apres son attaque", "« if able »", ["Puzzle.PutIntoPlay('pu014')"],
       ["Puzzle.EnemyAttacks('pu014', '01001a')"], {"engage": [["pu014", 0]], "degats_identite": 2}, **SANS_DEFENSE),
    _l("pu014 Muse (Forced Interrupt) : le joueur ENTRE dans son lieu -> il s'engage avec lui",
       "« When a player enters Muse's location, he engages them »", [*ville(), "Puzzle.PutIntoPlay('pu014')", "Puzzle.AttacherAuLieu('pu014', 'pu031')"],
       ["Puzzle.DeplacerDansLaVille((0, 1))"], {"engage": [["pu014", 0]], "attache_a": [["pu014", None]]}),
    _l("pu014 Muse (Boost) : revelee comme carte de boost -> elle entre en jeu, engagee avec le joueur", "« ★ Boost : Reveal this card »",
       [], ["Puzzle.Boost('pu014')"], {"engage": [["pu014", 0]]}),
    # ------------------------------------------------------------------------------------------------ pu015 Screwball
    _l("pu015 Screwball (Forced Interrupt) : vaincue avec EXCES de degats (3 PV, 3 + 2) -> elle n'est PAS vaincue, PV remis, attachee a Hell's Kitchen, hors engagement",
       "« When Screwball would be defeated with excess damage, reset her hit points instead. Attach her to an unoccupied location »",
       [*ville(), "Puzzle.PutIntoPlay('pu015')"], ["Puzzle.Damage('pu015', 5)"],
       {"attache_a": [["pu015", "pu030"]], "engage": [["pu015", None]]}),
    _l("pu015 Screwball : elle revient ensuite a PLEIN de PV (3) quand un joueur entre dans son lieu", "PV remis a l'attache",
       [*ville(), "Puzzle.PutIntoPlay('pu015')"], ["Puzzle.Damage('pu015', 5)", "Puzzle.PlacerDansLaVille((0, 0))"],
       {"engage": [["pu015", 0]], "pv_de": [["pu015", 3]]}),
    _l("pu015 Screwball, TEMOIN : vaincue par un coup EXACT (3 degats sur 3 PV) -> aucun exces : elle est vaincue (defausse de rencontre)",
       "« with EXCESS damage » seulement", [*ville(), "Puzzle.PutIntoPlay('pu015')"], ["Puzzle.Damage('pu015', 3)"],
       {"defausse_rencontre": ["pu015"], "attache_a": [["pu015", None]]}),
    _l("pu015 Screwball : exces mais aucun lieu (plus de ville) -> elle reste engagee, PV remis (3)", "« if able »",
       ["Puzzle.PutIntoPlay('pu015')"], ["Puzzle.Damage('pu015', 5)"], {"engage": [["pu015", 0]], "pv_de": [["pu015", 3]]}),
    _l("pu015 Screwball (Forced Interrupt) : le joueur ENTRE dans son lieu -> elle s'engage avec lui", "« she engages them »",
       [*ville(), "Puzzle.PutIntoPlay('pu015')", "Puzzle.AttacherAuLieu('pu015', 'pu031')"], ["Puzzle.DeplacerDansLaVille((0, 1))"],
       {"engage": [["pu015", 0]], "attache_a": [["pu015", None]]}),
    # ------------------------------------------------------------------------------------------------ pu022 Like and Subscribe!
    _l("pu022 Like and Subscribe! (When Revealed) : trouve Screwball (dans le deck de rencontre), la revele, et l'attache a Hell's Kitchen",
       "« Find and reveal Screwball. Attach her to an unoccupied location, if able »", [*ville()], ["Puzzle.Reveal('pu022')"],
       {"attache_a": [["pu015", "pu030"]], "engage": [["pu015", None]]}, deck=("01105", "pu015")),
    _l("pu022 Like and Subscribe! : aucun lieu libre (plus de ville) -> Screwball reste engagee avec le joueur", "« if able »",
       [], ["Puzzle.Reveal('pu022')"], {"engage": [["pu015", 0]]}, deck=("01105", "pu015")),
    _l("pu022 Like and Subscribe! : les allies entrent en jeu EPUISES (Gwen Stacy... : un allie quelconque, 01075)", "« Allies enter play exhausted »",
       [*ville()], ["Puzzle.Reveal('pu022')", "Puzzle.PutIntoPlay('01075', under_control=True)"], {"exhausted": ["01075"]}),
    _l("pu022 Like and Subscribe!, TEMOIN : SANS la manigance, le meme allie entre PRET", "ligne de base",
       [*ville()], ["Puzzle.PutIntoPlay('01075', under_control=True)"], {"pret": ["01075"]}),
    _l("pu022 Like and Subscribe! (Boost) : revelee comme carte de boost -> elle entre en jeu (manigance annexe)", "« ★ Boost : Reveal this card »",
       [], ["Puzzle.Boost('pu022')"], {"en_jeu": ["pu022"], "engage": [["pu015", 0]]}, deck=("01105", "pu015")),
    # ------------------------------------------------------------------------------------------------ FAQ « Collaboration » (Teamwork)
    _l("FAQ Collaboration : un sbire ACOLYTE d'un AUTRE territoire (Exodus engage avec le 2e joueur, a Hell's Kitchen) suffit -> Fabian Cortez (Teamwork ACOLYTE) s'active : le heros prend des degats",
       "FAQ : les sbires « en jeu » ne sont PAS limites a un territoire",
       [*ville()], ["Puzzle.PlacerDansLaVille((0, 0), 1)", "Puzzle.PutIntoPlay('37032')", "Puzzle.Engage('37032', 1)", "Puzzle.Reveal('32159')"],
       {"degats_identite_min": 1}, deck=("32159", "01105"), heros2="spider_man", **SANS_DEFENSE),
    _l("FAQ Collaboration : un sbire ACOLYTE ATTACHE a un lieu (Exodus sous Hell's Kitchen, « reste en jeu ») suffit aussi", "un sbire attache est en jeu",
       [*ville(), "Puzzle.PutIntoPlay('37032')", "Puzzle.AttacherAuLieu('37032', 'pu030')"], ["Puzzle.Reveal('32159')"],
       {"degats_identite_min": 1}, deck=("32159", "01105"), **SANS_DEFENSE),
    _l("FAQ Collaboration, TEMOIN : aucun autre ACOLYTE -> Fabian ne s'active pas (0 degat)", "ligne de base",
       [*ville()], ["Puzzle.Reveal('32159')"], {"degats_identite": 0}, deck=("32159", "01105")),
]


VERIFICATIONS = r'''
def lieu_etat(monde, aides):
    """Cles propres : `engage` [[card_id, indice du joueur | None]], `attache_a` [[card_id, card_id du lieu | None]], `pv_de` [[card_id, PV]],
    `distribuees` [[indice du joueur, nombre de cartes de rencontre distribuees]] ; le reste va a `big_etat`."""
    from game.operate.ville import Ville
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    soucis = []
    for card_id, voulu in attendu.get("engage") or []:
        face = aides["par_id"](monde, card_id)
        vu = None
        if face is not None and face.IsInPlay():
            joueur = getattr(face, "engaged_player", None)
            vu = None if joueur is None else joueur.player_id
        if vu != voulu:
            soucis.append(f"{card_id} engage avec {vu} (attendu {voulu})")
    for card_id, voulu in attendu.get("attache_a") or []:
        vu = None
        for lieu in Ville.Lieux(monde):
            if any(f.paper.card_id == card_id and Ville.Hote(f) is lieu for f in lieu.GetPlacedCardArea().GetAll()):
                vu = lieu.paper.card_id
        if vu != voulu:
            soucis.append(f"{card_id} attache a {vu} (attendu {voulu})")
    for card_id, voulu in attendu.get("pv_de") or []:
        face = aides["par_id"](monde, card_id)
        if face is None or not face.IsInPlay():
            soucis.append(f"{card_id} pas en jeu (PV)")
        elif face.health != voulu:
            soucis.append(f"{card_id} a {face.health} PV (attendu {voulu})")
    for indice, voulu in attendu.get("distribuees") or []:
        n = len(monde.const_players[indice].dealt_encounter_cards.GetAll())
        if n != voulu:
            soucis.append(f"joueur {indice} : {n} carte(s) de rencontre distribuee(s) (attendu {voulu})")
    propres = ("engage", "attache_a", "pv_de", "distribuees")
    cas["attendu"] = {k: v for k, v in attendu.items() if k not in propres}
    try:
        if cas["attendu"]:
            ok, msg = big_etat(monde, aides)
            if not ok:
                soucis.append(msg)
    finally:
        cas["attendu"] = attendu
    return (False, " ; ".join(soucis)) if soucis else (True, "cartes liees aux lieux conformes")
'''
