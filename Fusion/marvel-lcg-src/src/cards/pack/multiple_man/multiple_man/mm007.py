from . import *

# Someone's Got This : EVENEMENT, cout 2, [energy] (mm006) ou [physical] (mm007). DUPLICATE. SUPERPOWER. THWART.
# Hero Action (thwart): Remove 2 threat from a scheme. Then, remove 1 threat from each scheme in play for each Dupe ally in play.
#
# CARTES DE REFERENCE : `ca010` (Sinister Flight : `RemoveThreatFromSchemes` + `.SetPlay().SetLabel('thwart').SetTarget(Scheme2)`), `lj019` (retirer de la menace de CHAQUE manigance :
#  `Worlds.FindCardsOnField(effect, card_type=Scheme2)`).
# TEXTE CONTRE CODE : « Then » : deux retraits distincts. « for EACH Dupe ally IN PLAY » : tous les Dupe en jeu (pas seulement les siens). DECISION UTILISATEUR (04/11) : seul un Dupe peut retirer
#  de la menace des complots « Only a Dupe ally... » : l'evenement les ignore (verrou `ThreatCannotBeRemovedFromWhile` pose par ces cartes). Chiffres : cout 2.


def GetAbilities() -> Sequence['Ability']:

    def someone(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        this.RemoveThreatFromSchemes(effect.targets, 2, effect)
        nombre = len(DupesEnJeu(effect))
        if nombre > 0:
            manigances = Worlds.FindCardsOnField(effect, card_type=Scheme2)
            if manigances:
                this.RemoveThreatFromSchemes(manigances, nombre, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            someone,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
