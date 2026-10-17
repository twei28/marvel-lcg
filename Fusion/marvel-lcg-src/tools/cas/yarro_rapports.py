# Rapports de bug de Yarro (n 85 a 93, 15-17/10/2026) : cas de non-regression.
CAS = [
    {
        "nom": "[yarro93] 16093 Nebula's Ship — Shoot the Thrusters! : 2 ressources depensees retirent 2 compteurs evasion",
        "pourquoi": ("rapport Yarro n93 (17/10/2026) : le Milano s'inclinait mais aucune ressource ne pouvait etre "
                     "depensee, les compteurs restaient"),
        "scenario": "rhino",
        "heros": "rocket_raccoon",
        "mise_en_place": ["Puzzle.PutIntoPlay('16142', under_control=True)",
                          "Puzzle.PutIntoPlay('16093')",
                          "Puzzle.Counter('16093', 'evasion', 2)"],
        "main_exclusive": ["01088", "01089"],
        "declencher": ["Puzzle.Action('16093')"],
        "payer_jusqu_a": 2,
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["16093", "evasion", 0]], "exhausted": ["16142"]},
    },
    {
        "nom": "[yarro93] 16142 Milano — TEMOIN : hors de ce cout, sa ressource [wild] paie toujours une carte",
        "pourquoi": "le filtre ajoute pour Nebula's Ship ne doit retirer le Milano que du cout qui l'incline",
        "scenario": "rhino",
        "heros": "rocket_raccoon",
        "mise_en_place": ["Puzzle.PutIntoPlay('16142', under_control=True)"],
        "main_exclusive": ["16038"],
        "declencher": [],
        "jouer": ["16038"],
        "payer_avec": ["16142"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["16038"], "exhausted": ["16142"]},
    },
    {
        "nom": "[yarro85] 16033 Salvage — la carte remise sur le deck est CONNUE mais pas REGARDEE (looked_at_by vide)",
        "pourquoi": ("rapport Yarro n85 (15/10/2026) : la fenetre « Cartes regardees » se rouvrait a chaque Salvage, "
                     "le plateau prenant toute carte connue du deck pour une carte regardee"),
        "scenario": "rhino",
        "heros": "rocket_raccoon",
        "mise_en_place": ["Puzzle.Gain('16038')"],  # defaussee pour de vrai par main_exclusive
        "main_exclusive": ["16033", "16039"],
        "declencher": [],
        "jouer": ["16039"],
        "payer_avec": ["16033"],
        "cibles": ["16038"],
        "verifier": "yarro_deck_regardees",
        "attendu": {"dessus": "16038", "connue": True, "regardee": False},
    },
    {
        "nom": "[yarro85] Faces.LookAt — TEMOIN : 2 cartes regardees du deck portent looked_at_by, effacee quand la carte change de zone",
        "pourquoi": "la fenetre « Cartes regardees » doit toujours s'ouvrir pour un vrai « look at »",
        "scenario": "rhino",
        "heros": "rocket_raccoon",
        "mise_en_place": ["Puzzle.CreatePlayerDeck('16031', '16038', '16039')"],
        "declencher": [],
        "verifier": "yarro_regard_direct",
        "attendu": {},
    },
    {
        "nom": "[yarro85] 16033 Salvage — un SOUTIEN Tech (56012 Air Cover) n'est pas une cible : « a [tech] upgrade »",
        "pourquoi": ("texte imprime « put a [tech] UPGRADE from your discard pile on top of your deck » ; le script "
                     "ciblait toute carte Tech, soutiens compris (13 soutiens Tech joueur dans cards.json)"),
        "scenario": "rhino",
        "heros": "rocket_raccoon",
        "mise_en_place": ["Puzzle.Gain('56012')"],  # defaussee pour de vrai par main_exclusive
        "main_exclusive": ["16033", "16039"],
        "declencher": [],
        "jouer": ["16039"],
        "payer_avec": ["16033"],
        "verifier": "etat_attendu",
        "attendu": {"defausse": ["56012"], "en_jeu": ["16039"]},
    },
    {
        "nom": "[yarro89] 16125 The Poison — debut de tour : 1 compteur poison puis 1 degat par compteur (1, puis 2)",
        "pourquoi": ("rapport Yarro n89/90 (16/10/2026, « le compteur de poison ne fonctionne pas ») : le journal montre "
                     "les degats empeches par Forcefield Generator. Ce cas mesure le Poison SANS Forcefield"),
        "scenario": "rhino",
        "heros": "rocket_raccoon",
        "mise_en_place": ["Puzzle.ChangeForm('16029b')", "Puzzle.PutIntoPlay('16125')"],
        "declencher": [],
        "verifier": "yarro_poison",
        "attendu": {"degats": [1, 3], "poison": [1, 2], "energie": None},
    },
    {
        "nom": "[yarro89] 16125 The Poison + 31019 Forcefield Generator — les degats du poison sont empeches, l energie baisse (1, puis 2)",
        "pourquoi": "la lecture du journal de Yarro : Forcefield empeche 1, puis 2, puis 3 degats ; aucun degat sur Rocket",
        "scenario": "rhino",
        "heros": "rocket_raccoon",
        "mise_en_place": ["Puzzle.ChangeForm('16029b')", "Puzzle.PutIntoPlay('31019', under_control=True)",
                          "Puzzle.PutIntoPlay('16125')"],
        "declencher": [],
        "verifier": "yarro_poison",
        "attendu": {"degats": [0, 0], "poison": [1, 2], "energie": [5, 3]},
    },
]

VERIFICATIONS = r'''
def yarro_deck_regardees(monde, aides):
    """Le dessus du deck du joueur 0 : `connue` (visible_for_players) et `regardee` (looked_at_by)."""
    attendu = aides["cas"].get("attendu") or {}
    joueur = monde.players[0]
    dessus = joueur.player_deck.GetTop()
    if dessus is None:
        return False, "deck vide"
    if dessus.paper.card_id != attendu["dessus"]:
        return False, f"dessus du deck = {dessus.paper.card_id} (attendu {attendu['dessus']})"
    rendu = dessus.card.Render()
    connue = 0 in rendu.visible_for_players
    regardee = 0 in rendu.looked_at_by
    if connue != attendu["connue"] or regardee != attendu["regardee"]:
        return False, f"connue={connue} regardee={regardee} (attendu {attendu['connue']}/{attendu['regardee']})"
    return True, "etat conforme"


def yarro_regard_direct(monde, aides):
    from game.effect.rule import DebugRule
    from game.operate.faces import Faces
    joueur = monde.players[0]
    effet = DebugRule(monde.object_manager.card_dict[0].face)
    deck = joueur.player_deck
    deux = [deck.cards[-1].face, deck.cards[-2].face]
    if any(0 in f.card.Render().looked_at_by for f in deux):
        return False, "deja regardees avant le look at"
    Faces.LookAt(deux, joueur, effet)
    if not all(f.card.Render().looked_at_by == [0] for f in deux):
        return False, f"apres look at : {[f.card.Render().looked_at_by for f in deux]}"
    premiere = deux[0]
    Faces.MoveAllTo([premiere], joueur.hand_cards, effet)
    Faces.MoveAllToDeck([premiere], deck, "Top", effet)
    if premiere.card.Render().looked_at_by:
        return False, "le regard a survecu a un aller-retour par la main"
    if deux[1].card.Render().looked_at_by != [0]:
        return False, "la seconde carte, restee dans le deck, a perdu son regard"
    return True, "etat conforme"


def yarro_poison(monde, aides):
    """Deux debuts de tour du joueur 0 : degats cumules, compteurs poison, energie de Forcefield."""
    from game.message import Message
    attendu = aides["cas"].get("attendu") or {}
    joueur = monde.players[0]
    identite = aides["identite"](monde)
    poison = aides["par_id"](monde, "16125")
    if poison is None:
        return False, "The Poison introuvable en jeu"
    champ = aides["par_id"](monde, "31019")
    pv0 = identite.health
    mesures = []
    for _ in range(2):
        Message.WhenPlayerTurnBegin(joueur).Send()
        mesures.append((pv0 - identite.health, poison.GetCounters("poison"),
                        champ.GetCounters("energy") if champ is not None and champ.IsInPlay() else None))
    degats = [m[0] for m in mesures]
    compteurs = [m[1] for m in mesures]
    energie = [m[2] for m in mesures] if attendu.get("energie") is not None else None
    if degats != attendu["degats"] or compteurs != attendu["poison"] or energie != attendu.get("energie"):
        return False, f"degats={degats} poison={compteurs} energie={energie} (attendu {attendu})"
    return True, "etat conforme"
'''
