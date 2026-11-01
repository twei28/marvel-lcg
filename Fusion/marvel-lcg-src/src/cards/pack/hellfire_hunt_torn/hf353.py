from . import *

# Mental Paralysis (traitrise PSIONIC SKILL, Surge, Boost 3 + [star]). « Surge. When Revealed : You are stunned and confused. [star] Boost : You are stunned and confused. »
# Surge : natif (`desc`, fiche surge.md : RR 1.8, la carte DISTRIBUE une carte face cachee au joueur). Cartes de reference : 41029 / hf308 (`Faces.GiveStatus([identite], ...)`).
# ⚠ « You » = l'identite du joueur qui revele / qui subit l'activation (`message.GetToPlayer()`), pas tous les joueurs.


def _etourdir_et_confondre(effect: 'Effect', joueur: 'Player|None') -> None:
    identite = joueur.GetIdentity() if joueur is not None else None
    if identite is not None:
        Faces.GiveStatus([identite], "Stunned", effect)
        Faces.GiveStatus([identite], "Confused", effect)


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        _etourdir_et_confondre(effect, message.GetToPlayer())

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        _etourdir_et_confondre(effect, message.GetToPlayer())

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
