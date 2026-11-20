# Cas test_capacites : « Captured by Hydra » (04107, Taskmaster) + tirage manuel, noms « [capture_hydra] » / « [tirage_manuel] ».
# Rapport 131 (14/11/2026) : l'allie CAPTIVE pose sous la manigance apparaissait FACE VISIBLE au joueur
# (`PlaceCardHere(.., False, ..)` garde « connu » de qui voyait la carte dans la zone de cote). Et la suggestion du joueur : tirer
# SOI-MEME la carte « au hasard » parmi des dos melanges : regle de partie `tirage_manuel` (decochee par defaut), `Rand.RandomCards`.
SC = "rhino"
CAPTIFS = ["Puzzle.FindOrCreateFace('04097')", "Puzzle.FindOrCreateFace('04098')"]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": nom, "pourquoi": pourquoi, "scenario": SC, "heros": "spider_man", "mise_en_place": mise,
           "declencher": declencher, "verifier": "capture_hydra_rendu", "accepter_choix": True, "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    _c("[capture_hydra] 04107 : l'allie CAPTIVE tire est pose sous la manigance, face cachee ET inconnu du joueur",
       "« Place 1 random set-aside Captive ally facedown beneath this scheme » : le joueur ne doit pas voir qui c'est",
       CAPTIFS[:1], ["Puzzle.Reveal('04107')"], {"hote": "04107", "captifs": ["04097"], "dessous": 1, "questions": 0}),
    _c("[tirage_manuel] 04107 + regle cochee : le joueur designe lui-meme le captif (1 question), il va dessous, face cachee, inconnu",
       "regle `tirage_manuel` : `Rand.RandomCards` presente les captifs de cote en dos melanges, le joueur en designe un",
       CAPTIFS, ["Puzzle.Reveal('04107')"], {"hote": "04107", "captifs": ["04097", "04098"], "dessous": 1, "questions": 1},
       regles=["tirage_manuel"]),
    _c("[tirage_manuel] 04107 + regle DECOCHEE : aucune question, le moteur tire (defaut, sauvegardes anciennes intactes)",
       "sans la regle, rien ne change : pas de question, un captif dessous",
       CAPTIFS, ["Puzzle.Reveal('04107')"], {"hote": "04107", "captifs": ["04097", "04098"], "dessous": 1, "questions": 0}),
    _c("[tirage_manuel] defausse au hasard de la main + regle cochee : 1 question, une carte part a la defausse",
       "`DiscardRandomHandCards` -> `GetRandomHandCards` -> `Rand.RandomCards` : le joueur designe la carte de sa main",
       ["Puzzle.EmptyHand()", "Puzzle.CreateHandCards('01090', '01091', '01092')"], ["Puzzle.DiscardAtRandom(1)"],
       {"main_apres": 2, "questions": 1}, regles=["tirage_manuel"]),
    _c("[tirage_manuel] defausse au hasard de la main + regle DECOCHEE : aucune question",
       "defaut inchange", ["Puzzle.EmptyHand()", "Puzzle.CreateHandCards('01090', '01091', '01092')"], ["Puzzle.DiscardAtRandom(1)"],
       {"main_apres": 2, "questions": 0}),
]

VERIFICATIONS = r'''
def capture_hydra_rendu(monde, aides):
    att = aides["cas"]["attendu"]
    soucis, vus = [], []
    joueur = monde.players[0]
    questions = getattr(joueur, "nb_tirages_manuels", 0)
    if questions != att["questions"]:
        soucis.append(f"{questions} question(s) de tirage manuel (attendu {att['questions']})")
    if "hote" in att:
        hote = None
        for f in monde.object_manager.card_dict.values():
            if f.face.paper.card_id == att["hote"]:
                hote = f
        if hote is None:
            return False, "manigance absente"
        place = hote.face.GetPlacedCardArea()
        vus.append(f"hote_aire={hote.area!r} captifs_aires={[ (f.face.paper.card_id, repr(f.area)) for f in monde.object_manager.card_dict.values() if f.face.paper.card_id in att['captifs']]}")
        dessous = [f for f in monde.object_manager.card_dict.values()
                   if f.face.paper.card_id in att["captifs"] and f.area == place]
        if len(dessous) != att["dessous"]:
            soucis.append(f"{len(dessous)} captif(s) sous la manigance (attendu {att['dessous']})")
        for f in dessous:
            r = f.Render()
            vus.append(f"{f.face.paper.card_id}: is_face_up={r.is_face_up} connu_de={list(r.visible_for_players)}")
            if r.is_face_up or list(r.visible_for_players):
                soucis.append(f"{f.face.paper.card_id} est visible du joueur")
    if "main_apres" in att:
        n = len(joueur.hand_cards.Get())
        vus.append(f"main = {n}")
        if n != att["main_apres"]:
            soucis.append(f"main = {n} (attendu {att['main_apres']})")
    return (False, " ; ".join(soucis)) if soucis else (True, " ; ".join(vus) or "ok")
'''
