# Cas test_capacites du scenario BEBOP & ROCKSTEADY (TMNT Villains v3, Inkwire, prefixe `tk`).
SC = "bebop_rocksteady"
SCX = "bebop_rocksteady_expert"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01105', '01105', '01105', '01105')"]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    if not cle.pop("avec_boost", False):
        mise = SANS_BOOST + list(mise)
    cas = {"nom": "[bebop] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "bb_etat"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    _c("tk005a mise en place : deux vilains, environnement, annexe, deux Temper accroches",
       "Setup du complot : Bebop et Rocksteady en jeu, tk006a, tk101, Hog Wild sur Bebop, Rhino Rage sur Rocksteady",
       [], [],
       {"en_jeu": ["tk001a", "tk003a", "tk006a", "tk007a", "tk008a", "tk101"],
        "attache": [["tk007a", "tk001a"], ["tk008a", "tk003a"]]}),
    _c("tk007a Hog Wild : +1 ATK a Bebop par compteur knucklehead (2 compteurs -> ATK 2)",
       "« Bebop gets +1 ATK for each knucklehead counter here »",
       ["Puzzle.Counter('tk007a', 'knucklehead', 2)"], [],
       {"attaque": [["tk001a", 2]], "compteurs_sur": [["tk007a", "knucklehead", 2]]}),
    _c("tk007a Hog Wild : sans compteur, ATK 0 (ligne de base)",
       "contre-cas : Bebop A1 a ATK 0",
       [], [], {"attaque": [["tk001a", 0]]}),
    _c("tk007a Hog Wild : Special = 1 compteur (apres 1 degat sur Bebop)",
       "Reponse Forcee de tk001a : resoudre le Special du Temper",
       ["Puzzle.Damage('tk001a', 1)"], [],
       {"compteurs_sur": [["tk007a", "knucklehead", 1]], "degats": [["tk001a", 1]]}),
    _c("tk007a Hog Wild : a 3 compteurs il se retourne sur Headfirst (ENRAGED, +3 ATK, trait ENRAGED au vilain)",
       "« If there are at least 3 knucklehead counters here, flip this card to its ENRAGED side »",
       ["Puzzle.Counter('tk007a', 'knucklehead', 2)"], ["Puzzle.Damage('tk001a', 1)"],
       {"en_jeu": ["tk007b"], "absents": ["tk007a"], "attache": [["tk007b", "tk001a"]],
        "compteurs_sur": [["tk007b", "knucklehead", 3]], "trait_de": [["tk001a", "ENRAGED", True]],
        "attaque": [["tk001a", 3]]}),
]

CAS += [
    # ===================================================================== villains ALERT : phase du mechant
    _c("tk001a Bebop ALERT : debut de phase, sans compteur -> 1 menace sur le complot (et Rocksteady : 1 degat)",
       "« remove 1 knucklehead counter ... or place 1 threat on the main scheme » : aucun compteur, seule l'option menace reste",
       [], ["Puzzle.BeginVillainPhase()"],
       {"menace_de": [["tk005b", 1]], "degats_identite": 1}),
    _c("tk001a Bebop ALERT : debut de phase avec compteurs -> retire 1 compteur (option par defaut), pas de menace",
       "option 1 offerte seulement s'il y a un compteur ; le pilote prend la premiere option",
       ["Puzzle.Counter('tk007a', 'knucklehead', 2)"], ["Puzzle.BeginVillainPhase()"],
       {"compteurs_sur": [["tk007a", "knucklehead", 1]], "menace_de": [["tk005b", 0]]}),
    _c("tk001a Bebop ALERT : le choix « menace » est possible meme avec des compteurs",
       "les deux options ouvertes : on force la seconde",
       ["Puzzle.Counter('tk007a', 'knucklehead', 2)"], ["Puzzle.BeginVillainPhase()"],
       {"compteurs_sur": [["tk007a", "knucklehead", 2]], "menace_de": [["tk005b", 1]]},
       choisir_option="Place_1_threat_on_the_main_scheme"),
    _c("tk002a Bebop ALERT (expert) : 2 menaces sur le complot",
       "stade B1 : « place 2 threat on the main scheme »",
       [], ["Puzzle.BeginVillainPhase()"],
       {"menace_de": [["tk005b", 2]]}, scenario=SCX),
    _c("tk003a Rocksteady ALERT : debut de phase -> carte Robuste + 1 degat au premier joueur (aucun compteur)",
       "« give Rocksteady a tough status card. Remove 1 counter ... or deal 1 damage to the first player »",
       [], ["Puzzle.BeginVillainPhase()"],
       {"degats_identite": 1, "statuts_sur": [["tk003a", "tough", 1]]}),
    _c("tk003a Rocksteady ALERT : avec un compteur Rhino Rage -> le retire (defaut), aucun degat",
       "option 1 (compteur) offerte et prise par defaut",
       ["Puzzle.Counter('tk008a', 'knucklehead', 1)"], ["Puzzle.BeginVillainPhase()"],
       {"compteurs_sur": [["tk008a", "knucklehead", 0]], "degats_identite": 0, "statuts_sur": [["tk003a", "tough", 1]]}),
    _c("tk004a Rocksteady ALERT (expert) : 2 degats au premier joueur",
       "stade B1 : « deal 2 damage to the first player »",
       [], ["Puzzle.BeginVillainPhase()"],
       {"degats_identite": 2}, scenario=SCX),
    # ===================================================================== Reponse Forcee « apres avoir subi des degats »
    _c("tk003a Rocksteady ALERT : apres 1 degat, Special de Rhino Rage = 1 compteur",
       "« After Rocksteady takes damage, resolve the Special ability on the RHINO attachment »",
       ["Puzzle.Damage('tk003a', 1)"], [],
       {"compteurs_sur": [["tk008a", "knucklehead", 1]]}),
    _c("tk003a Rocksteady ALERT : une Reponse par EVENEMENT de degats (2 evenements -> 2 compteurs)",
       "chaque instance de degats declenche la Reponse Forcee",
       [], ["Puzzle.Damage('tk003a', 1)", "Puzzle.Damage('tk003a', 1)"],
       {"compteurs_sur": [["tk008a", "knucklehead", 2]]}),
    _c("tk001b Bebop K.O. : PAS de Reponse Forcee (le texte n'est imprime que sur la face ALERT)",
       "contre-cas : Bebop K.O. blesse -> Hog Wild ne recoit rien",
       ["Puzzle.Flip('tk001a')"], ["Puzzle.Damage('tk001b', 1)"],
       {"compteurs_sur": [["tk007a", "knucklehead", 0]]}),
    # ===================================================================== villains K.O.
    _c("tk001b Bebop K.O. : activation = retire 1 compteur a la place (pas d'attaque), reste K.O. s'il en reste",
       "« When Bebop activates, remove 1 knucklehead counter from the HOG attachment instead »",
       ["Puzzle.Counter('tk007a', 'knucklehead', 2)", "Puzzle.Flip('tk001a')", "Puzzle.Exhaust('01001a')"],
       ["Puzzle.Attack('tk001b')"],
       {"en_jeu": ["tk001b"], "compteurs_sur": [["tk007a", "knucklehead", 1]], "degats_identite": 0}),
    _c("tk001b Bebop K.O. : dernier compteur retire -> se retourne sur ALERT",
       "« If there are no knucklehead counters there, flip Bebop to his ALERT side » : lecture sequentielle (retire puis teste)",
       ["Puzzle.Counter('tk007a', 'knucklehead', 1)", "Puzzle.Flip('tk001a')", "Puzzle.Exhaust('01001a')"],
       ["Puzzle.Attack('tk001b')"],
       {"en_jeu": ["tk001a"], "absents": ["tk001b"], "compteurs_sur": [["tk007a", "knucklehead", 0]], "degats_identite": 0}),
    _c("tk001b Bebop K.O. : sans aucun compteur, l'activation le reveille aussi",
       "« If there are no knucklehead counters there » : zero compteur au depart",
       ["Puzzle.Flip('tk001a')", "Puzzle.Exhaust('01001a')"], ["Puzzle.Attack('tk001b')"],
       {"en_jeu": ["tk001a"], "absents": ["tk001b"], "degats_identite": 0}),
    _c("tk002b Bebop K.O. (expert) : retire 2 compteurs",
       "stade B2 : « remove 2 knucklehead counters »",
       ["Puzzle.Counter('tk007a', 'knucklehead', 3)", "Puzzle.Flip('tk002a')", "Puzzle.Exhaust('01001a')"],
       ["Puzzle.Attack('tk002b')"],
       {"compteurs_sur": [["tk007a", "knucklehead", 1]], "en_jeu": ["tk002b"]}, scenario=SCX),
    _c("tk003b Rocksteady K.O. : retire 1 compteur de Rhino Rage et reste K.O.",
       "meme mecanique que Bebop, sur l'attachement RHINO",
       ["Puzzle.Counter('tk008a', 'knucklehead', 2)", "Puzzle.Flip('tk003a')", "Puzzle.Exhaust('01001a')"],
       ["Puzzle.Attack('tk003b')"],
       {"compteurs_sur": [["tk008a", "knucklehead", 1]], "en_jeu": ["tk003b"], "degats_identite": 0}),
    _c("tk004b Rocksteady K.O. (expert) : 2 compteurs d'un coup, 1 seul disponible -> se reveille",
       "« remove 2 ... » avec un seul compteur : on retire ce qu'il y a, puis ALERT",
       ["Puzzle.Counter('tk008a', 'knucklehead', 1)", "Puzzle.Flip('tk004a')", "Puzzle.Exhaust('01001a')"],
       ["Puzzle.Attack('tk004b')"],
       {"en_jeu": ["tk004a"], "compteurs_sur": [["tk008a", "knucklehead", 0]]}, scenario=SCX),
    _c("tk001b Bebop K.O. ET etourdi : le statut passe d'abord (la carte Etourdi est retiree, les compteurs restent)",
       "FAQ de l'encart : « Status cards always take priority... you would remove the stun status card instead »",
       ["Puzzle.Counter('tk007a', 'knucklehead', 2)", "Puzzle.Flip('tk001a')", "Puzzle.Stun('tk001b')", "Puzzle.Exhaust('01001a')"],
       ["Puzzle.Attack('tk001b')"],
       {"statuts_sur": [["tk001b", "stunned", 0]], "compteurs_sur": [["tk007a", "knucklehead", 2]]}),
]


# Verification outillee du pack : etat_attendu (cles de base) + extensions lues sur les faces EN JEU.
VERIFICATIONS = r'''
def bb_etat(monde, aides):
    """Extensions de `etat_attendu` : attache [[carte, hote]], compteurs_sur [[id, nom, n]],
    menace_de [[id, n]], attaque [[id, n]], statuts_sur [[id, 'stunned'|'tough'|'confused', n]],
    vie [[id, pv_max]], absents [ids hors jeu], trait_de [[id, TRAIT, bool]], bascule : etat_attendu d'abord."""
    attendu = aides["cas"].get("attendu") or {}
    ok, msg = etat_attendu(monde, aides)
    soucis = [] if ok else [msg]
    par_id = aides["par_id"]
    for cid, hote in attendu.get("attache", []):
        f = par_id(monde, cid)
        if f is None:
            soucis.append(f"{cid} n'est pas en jeu"); continue
        b = f.bind_face
        got = getattr(getattr(b, "paper", None), "card_id", None) if b else None
        if got != hote:
            soucis.append(f"{cid} attache a {got} (attendu {hote})")
    for cid, nom, n in attendu.get("compteurs_sur", []):
        f = par_id(monde, cid)
        if f is None:
            soucis.append(f"{cid} n'est pas en jeu"); continue
        if f.GetCounters(nom) != n:
            soucis.append(f"{cid} compteurs {nom} = {f.GetCounters(nom)} (attendu {n})")
    for cid, n in attendu.get("menace_de", []):
        f = par_id(monde, cid)
        if f is None:
            soucis.append(f"{cid} n'est pas en jeu"); continue
        if f.threat != n:
            soucis.append(f"{cid} menace = {f.threat} (attendu {n})")
    for cid, n in attendu.get("attaque", []):
        f = par_id(monde, cid)
        if f is None:
            soucis.append(f"{cid} n'est pas en jeu"); continue
        if f.attack != n:
            soucis.append(f"{cid} ATK = {f.attack} (attendu {n})")
    for cid, n in attendu.get("vie", []):
        f = par_id(monde, cid)
        if f is None:
            soucis.append(f"{cid} n'est pas en jeu"); continue
        if f.max_health != n:
            soucis.append(f"{cid} PV max = {f.max_health} (attendu {n})")
    for cid, st, n in attendu.get("statuts_sur", []):
        f = par_id(monde, cid)
        if f is None:
            soucis.append(f"{cid} n'est pas en jeu"); continue
        v = getattr(f, st)
        if v != n:
            soucis.append(f"{cid} statut {st} = {v} (attendu {n})")
    for cid in attendu.get("absents", []):
        if par_id(monde, cid) is not None:
            soucis.append(f"{cid} est encore en jeu")
    for cid, tr, b in attendu.get("trait_de", []):
        f = par_id(monde, cid)
        if f is None:
            soucis.append(f"{cid} n'est pas en jeu"); continue
        if bool(f.HasTrait(tr)) != b:
            soucis.append(f"{cid} trait {tr} = {f.HasTrait(tr)} (attendu {b})")
    for cid in attendu.get("steady", []):
        f = par_id(monde, cid)
        if f is None:
            soucis.append(f"{cid} n'est pas en jeu"); continue
        if not f.IsSteady():
            soucis.append(f"{cid} n'est pas Steady")
    if "gagnee" in attendu:
        fini = bool(getattr(monde, "is_game_over", False))
        gagne = fini and bool(monde.game_over.players_won)
        if (fini and gagne) != attendu["gagnee"]:
            soucis.append(f"partie finie={fini} gagnee={gagne} (attendu gagnee={attendu['gagnee']})")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "etat conforme"
'''
