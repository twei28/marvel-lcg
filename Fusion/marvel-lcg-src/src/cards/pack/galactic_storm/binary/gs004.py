from . import *

# Pursued by the Flame — EVENEMENT, cout 1, [energy]. SUPERPOWER. THWART. x2 (Binary 5/15, 6/15).
# Hero Action (thwart): Remove 2 threat from a scheme. If you have at least
#   [energy][energy] resources in your hand, ready Binary.
#
# Cartes de reference :
#  - **`core/01052`** : evenement de contre, `WhenInYourPlayTurn(HeroAction, op)
#    .SetPlay().SetLabel('thwart').SetTarget(Scheme2)` +
#    `this.RemoveThreatFromSchemes(effect.targets, n, effect)`.
#  - « ready your hero » : `Faces.ReadyAll([identite], effect)` (`an001a`, `ho011`).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « a scheme » : une cible, n'importe quelle manigance (principale ou annexe).
#  - « at least [energy][energy] RESOURCES in your hand » : au moins 2 ICONES
#    (une seule Energy Torrent suffit), comptees A LA RESOLUTION, la carte jouee
#    et les cartes depensees ayant quitte la main. Helper `EnergieEnMain`.
#  - « ready BINARY » : l'identite en forme heros (seule forme qui joue une Hero
#    Action).
#  - Pas de limite imprimee.


def GetAbilities() -> Sequence['Ability']:

    def poursuite(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        this.RemoveThreatFromSchemes(effect.targets, 2, effect)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is not None and EnergieEnMain(joueur) >= 2:
            Faces.ReadyAll([joueur.GetIdentity()], effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            poursuite,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
