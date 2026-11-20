# Cas test_capacites de gs163 Main Concern (Earth Under Siege, lot GS-7). Filtre `[eus] gs163`.

MEC_SOCLE = [
    "Puzzle.RemoveVillain('01094')",
    "Puzzle.SetVillainRule('Leftmost', 'PlayerChooses')",
]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[eus] gs163 " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", "rhino"),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "etat_attendu"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    _c("entree en jeu, 2 mechants a PV differents : attache au plus riche en PV (gs166, 6 restants) et pas "
       "au plus faible (gs170, 4 restants)",
       "« Attach to the villain with the most remaining hit points » : AttachToFaceWhenPutIntoPlay, "
       "most_remaining_hp=True",
       MEC_SOCLE + [
           "Puzzle.BuildVillainDeck('gs166','gs170')", "Puzzle.RevealNextVillain()", "Puzzle.RevealNextVillain()",
           "Puzzle.Damage('gs170', 2)",
       ], ["Puzzle.PutIntoPlay('gs163')"],
       {"en_jeu": ["gs163"], "attaches": [["gs166", "gs163"]]}),
    _c("entree en jeu, 1 SEUL mechant en jeu : gagne surge au lieu de s'attacher",
       "« If there is only 1 villain in play, this card gains surge » : selecteur sans candidat "
       "(check_effect_fn len(Villains.All())>1 faux) -> if_cannot_gain_surge",
       MEC_SOCLE + [
           "Puzzle.BuildVillainDeck('gs166')", "Puzzle.RevealNextVillain()",
       ], ["Puzzle.PutIntoPlay('gs163')"],
       {}, verifier="gs163_surge"),
    _c("Players cannot deal damage to OTHER villains : le joueur blesse le mechant NON hote -> 0 degat",
       "« Players cannot deal damage to other villains » : WhenDamageWouldBeDealtTo + SetBeInstead, "
       "condition message.trigger n'est pas effect.this.bind_face",
       MEC_SOCLE + [
           "Puzzle.BuildVillainDeck('gs166','gs170')", "Puzzle.RevealNextVillain()", "Puzzle.RevealNextVillain()",
           "Puzzle.Damage('gs170', 2)", "Puzzle.PutIntoPlay('gs163')",
       ], ["Puzzle.Damage('gs170', 3, source=Puzzle.FindOrCreateFace('01001a'))"],
       {"degats": [["gs170", 2]]}),
    _c("Players cannot deal damage to other villains : le joueur blesse le mechant HOTE -> degats normaux",
       "meme restriction, mais l'hote lui-meme n'est jamais vise par le blocage",
       MEC_SOCLE + [
           "Puzzle.BuildVillainDeck('gs166','gs170')", "Puzzle.RevealNextVillain()", "Puzzle.RevealNextVillain()",
           "Puzzle.Damage('gs170', 2)", "Puzzle.PutIntoPlay('gs163')",
       ], ["Puzzle.Damage('gs166', 3, source=Puzzle.FindOrCreateFace('01001a'))"],
       {"degats": [["gs166", 3]]}),
    _c("Boost : attache a gs166 (PV restants 6, puis reduits a 2), devient boost alors que gs170 (4 "
       "restants) est plus riche -> demenage vers gs170",
       "« [star] Boost: Attach to the villain with the most remaining hit points » : WhenCardBecomeBoost, "
       "re-attache au plus riche du moment (peut changer d'hote)",
       MEC_SOCLE + [
           "Puzzle.BuildVillainDeck('gs166','gs170')", "Puzzle.RevealNextVillain()", "Puzzle.RevealNextVillain()",
           "Puzzle.Damage('gs170', 2)", "Puzzle.PutIntoPlay('gs163')", "Puzzle.Damage('gs166', 4)",
       ], ["Puzzle.Boost('gs163')"],
       {"attaches": [["gs170", "gs163"]]}),
]

VERIFICATIONS = r'''
def gs163_surge(monde, aides):
    """gs163, branche « If there is only 1 villain in play, this card gains surge » : la carte reste
    hors jeu (pas d'hote) et porte surge=1."""
    face = aides["par_id"](monde, "gs163")
    if face is None:
        for objet in monde.object_manager.card_dict.values():
            f = getattr(objet, "face", None) or objet
            if getattr(getattr(f, "paper", None), "card_id", None) == "gs163":
                face = f
                break
    if face is None:
        return False, "gs163 introuvable"
    if not getattr(face, "surge", 0):
        return False, f"gs163.surge = {getattr(face, 'surge', None)} (attendu >= 1)"
    return True, f"surge = {face.surge}"
'''
