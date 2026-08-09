from . import *

# Crack the Case — custom « ekAugust »
# Play only if there is a side scheme in play.
# Action (thwart): Remove 2 threat from a scheme. If a side scheme is defeated
#   this way, ready Jessica Jones.

def GetAbilities() -> Sequence['Ability']:

    def crack_the_case(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        cibles = list(effect.targets)
        this.RemoveThreatFromSchemes(cibles, 2, effect)

        # « If a side scheme is defeated this way » : la manigance a quitte le
        # terrain pendant la resolution.
        # CORRECTIF (4/8/2026) : `IsInField` n'existe sur AUCUNE face du moteur. La carte PLANTAIT des qu'on visait une manigance
        # annexe, c'est-a-dire dans le seul cas ou sa seconde moitie compte.
        for cible in cibles:
            if SchemeSide2.IsType(cible) and not cible.IsInPlay():
                identity = effect.GetInitiator().GetIdentity()
                if identity:
                    Faces.ReadyAll([identity], effect)
                break

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            crack_the_case,
            conditions=[IsSideSchemeInPlay],
        ).SetPlay()
        .SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
