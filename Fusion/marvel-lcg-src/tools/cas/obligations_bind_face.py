# Cas test_capacites : OBLIGATIONS OFFICIELLES qui lisent l'identite de leur joueur par `GetBindFace()` (46024 Hot-Headed, Iceman ;
# 49027 Old Grievances, Magneto). Noms prefixes « [ob] » puis le card_id.
#
# Pourquoi (26/10/2026) : le correctif de `src/game/card/face/card_type/obligation.py` (A Questing, wt016, « attach this card to it »)
# a change `bind_face` / `GetBindFace` : une obligation ATTACHEE a un sbire se lit sur son hote, une obligation dans la zone du joueur
# se lit toujours sur l'identite. Ces deux obligations n'avaient AUCUN cas : elles pouvaient casser sans que rien ne rougisse.
#
# Montage : `Puzzle.Reveal('<obligation>')` pose l'obligation chez le joueur (comme en partie). Rhino 01094 est le vilain.
SC = "rhino"


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[ob] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC), "heros": cle.pop("heros"),
           "mise_en_place": list(mise), "declencher": declencher, "verifier": "etat_attendu", "attendu": attendu}
    cas.setdefault("regles", ["v16_all", "v18_all"])
    cas.update(cle)
    return cas


CAS = [
    # ============================================================ 46024 Hot-Headed (Iceman / Bobby Drake)
    _c("46024 Hot-Headed : apres avoir attache Frostbite a un ennemi, l'identite du joueur subit 1 degat",
       "« Forced Response: After you attach a Frostbite upgrade to an enemy, take 1 damage » : `this.GetBindFace().GetControlByPlayer()` "
       "doit rendre le joueur (obligation dans SA zone d'obligations) : 1 degat sur Bobby Drake",
       ["Puzzle.Reveal('46024')"], ["Puzzle.AttachReel('46002', '01094')"],
       {"degats": [["46001b", 1]]}, heros="iceman"),
    _c("46024 Hot-Headed : CONTRE-CAS sans l'obligation en jeu, Frostbite attache -> aucun degat",
       "meme geste, sans `Reveal('46024')` : l'identite reste intacte (le degat vient bien de l'obligation)",
       [], ["Puzzle.AttachReel('46002', '01094')"],
       {"degats": [["46001b", 0]]}, heros="iceman"),

    # ============================================================ 49027 Old Grievances (Magneto / Erik Lehnsherr)
    _c("49027 Old Grievances : apres Magnetic Pull, l'identite subit 1 degat par carte defaussee",
       "« Forced Response: After you use Magnetic Pull, take 1 damage for each card discarded by it » : MAGNETIC en tete du deck, "
       "donc 1 carte defaussee (la carte trouvee) : 1 degat sur Magneto. Lit `this.GetBindFace().GetControlByPlayer()`",
       ["Puzzle.ChangeToFace('49001b', '49001a')", "Puzzle.Reveal('49027')", "Puzzle.PutIntoDeck('49005')"],
       ["Puzzle.Action('49001a', 'Action')"],
       {"degats": [["49001a", 1]]}, heros="magneto"),
    _c("49027 Old Grievances : CONTRE-CAS sans l'obligation en jeu, Magnetic Pull -> aucun degat",
       "meme geste sans `Reveal('49027')` : Magneto ne subit rien",
       ["Puzzle.ChangeToFace('49001b', '49001a')", "Puzzle.PutIntoDeck('49005')"],
       ["Puzzle.Action('49001a', 'Action')"],
       {"degats": [["49001a", 0]]}, heros="magneto"),
]
