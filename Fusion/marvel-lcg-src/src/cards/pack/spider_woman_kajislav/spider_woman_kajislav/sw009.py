from . import *

# Web Formation — EVENEMENT, cout 2, RES [mental].
# PSIONIC. SUPERPOWER. THWART.
# Hero Action (thwart): Remove 2 threat from each scheme. Place 1 psionic web
#   counter on Spider-Woman for each [mental] resource you used to pay for this
#   card (to a maximum of 10).
#
# ⚠ ELLE FRAPPE TOUTES LES MANIGANCES, principale comprise — c'est la seule
# carte du pack qui le fasse, et ce qui la rend chere a 2.
#
# CARTE DE REFERENCE
#  - `ip025` * Ghost : `RemoveThreatFromSchemes("EachScheme", ...)`, le
#    litteral que le moteur comprend (card_face.py:703).
#
# TEXTE CONTRE CODE
#  ⚠ « from EACH scheme » : toutes, sans choix. Pas « a scheme ».
#  ⚠ Le retrait est INCONDITIONNEL : il ne se paie pas en compteurs. Ce sont
#    les compteurs qui viennent APRES, et seulement si l'on a paye en [mental].


def GetAbilities() -> Sequence['Ability']:

    def formation(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        this.RemoveThreatFromSchemes("EachScheme", 2, effect)
        PoserDesToiles(effect.GetInitiator(),
                       ToilesParRessourceMentale(effect, 1), effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            formation,
        ).SetPlay().SetLabel('thwart'),
    ]
