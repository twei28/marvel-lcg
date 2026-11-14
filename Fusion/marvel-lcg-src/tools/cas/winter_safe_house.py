# Cas test_capacites de la carte OFFICIELLE Safe House #30 (54007, Winter Soldier, prefixe de nom « [ws] ») : signalement du joueur
# du 26/10/2026 (« il n'a pas cherche de sbire et il n'a pas pioche »).
#  - le deck `winter_soldier` demarre en ALTER EGO (54001b) : l'Action d'alter ego du soutien est donc offerte tout de suite ;
#  - Rhino 01094 est le vilain, 01110 Hydra Bomber un sbire (2 PV, sans Guard), 01098 un filler de deck de rencontre ;
#  - ⚠ `main_exclusive` DEFAUSSE la main de depart : avec ["01090"], la main vaut 1 carte avant l'Action.
SC = "rhino"
SBIRE = "01110"
FILLER = "01098"


def _deck(*ids):
    return ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck(" + ", ".join(f"'{i}'" for i in ids) + ")"]


def _c(nom, pourquoi, mise, attendu, **cle):
    cas = {"nom": "[ws] " + nom, "pourquoi": pourquoi, "scenario": SC, "heros": "winter_soldier",
           "mise_en_place": mise + ["Puzzle.PutIntoPlay('54007', under_control=True)"],
           "declencher": ["Puzzle.Action('54007', 'AlterEgoAction')"], "verifier": "ws_etat", "attendu": attendu}
    cas.setdefault("regles", ["v16_all", "v18_all"])
    cas.update(cle)
    return cas


CAS = [
    _c("54007 Safe House #30 : un sbire au FOND du deck de rencontre -> il entre en jeu engage, 1 carte piochee, Safe House inclinee",
       "« search the encounter deck for a minion and put it into play engaged with you. Then, draw 1 card »",
       _deck(*([FILLER] * 5), SBIRE),
       {"ws_sbire_engage": SBIRE, "exhausted": ["54007"], "taille_main": 2}, main_exclusive=["01090"], accepter_choix=True),
    _c("54007 Safe House #30 : aucun sbire dans le deck -> PAS de pioche (RR « Then »), et le joueur en est AVERTI (bulle `choix_uniques`)",
       "RR « Then » : la suite ne se resout que si la partie avant « Then » s'est resolue (rien a mettre en jeu) ; decision de l'utilisateur du 26/10/2026 : pas de pioche mais le jeu le dit",
       _deck(*([FILLER] * 6)),
       {"ws_aucun_sbire": True, "exhausted": ["54007"], "taille_main": 1,
        "ws_avis": "No minion in the encounter deck: no card is drawn."}, main_exclusive=["01090"], accepter_choix=True),
    _c("54007 Safe House #30 : avec un sbire, AUCUN avis « pas de pioche » n'est publie",
       "contre-cas : l'avis n'existe que lorsque la recherche ne trouve rien",
       _deck(*([FILLER] * 5), SBIRE),
       {"ws_sbire_engage": SBIRE, "taille_main": 2, "ws_pas_d_avis": True}, main_exclusive=["01090"], accepter_choix=True),
]


VERIFICATIONS = r'''
def ws_etat(monde, aides):
    """Cles propres : `ws_sbire_engage` (card_id du sbire attendu en jeu ET engage avec le joueur, et plus dans le deck de rencontre),
    `ws_aucun_sbire` (aucun sbire en jeu) ; le reste va a etat_attendu."""
    from game.card.face.card_type import Minion
    from game.operate.worlds import Worlds
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    soucis = []
    joueur = monde.players[0]
    sbires = []
    for objet in monde.object_manager.card_dict.values():
        face = getattr(objet, "face", None)
        if face is not None and face.IsInPlay() and Minion.IsType(face):
            sbires.append(face)
    voulu = attendu.get("ws_sbire_engage")
    if voulu:
        trouves = [m for m in sbires if getattr(m.paper, "card_id", None) == voulu]
        if not trouves:
            soucis.append(f"{voulu} pas en jeu (sbires en jeu : {[getattr(m.paper, 'card_id', None) for m in sbires]})")
        elif not any(m.GetEngagedPlayer() == joueur for m in trouves):
            soucis.append(f"{voulu} est en jeu mais pas engage avec le joueur")
        deck = [getattr(f.paper, "card_id", None) for f in Worlds.GetEncounterDeckCards(monde)]
        if voulu in deck:
            soucis.append(f"{voulu} est encore dans le deck de rencontre")
    if attendu.get("ws_aucun_sbire") and sbires:
        soucis.append(f"des sbires sont en jeu alors que le deck n'en contenait aucun : {[getattr(m.paper, 'card_id', None) for m in sbires]}")
    avis = [c.get("texte") for c in getattr(monde.stat, "choix_uniques", []) if c.get("texte")]
    if attendu.get("ws_avis") and attendu["ws_avis"] not in avis:
        soucis.append(f"l'avis « {attendu['ws_avis']} » n'a pas ete publie (avis : {avis})")
    if attendu.get("ws_pas_d_avis") and avis:
        soucis.append(f"un avis a ete publie alors qu'un sbire etait trouve : {avis}")
    propres = ("ws_sbire_engage", "ws_aucun_sbire", "ws_avis", "ws_pas_d_avis")
    reste = {k: v for k, v in attendu.items() if k not in propres}
    copie = dict(aides); copie["cas"] = dict(cas); copie["cas"]["attendu"] = reste
    ok, message = etat_attendu(monde, copie)
    if not ok:
        soucis.append(message)
    if soucis:
        return False, " ; ".join(soucis)
    return True, message
'''
