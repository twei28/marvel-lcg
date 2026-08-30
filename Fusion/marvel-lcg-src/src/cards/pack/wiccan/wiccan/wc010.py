from . import *

# Magic Portal (2/2) — exemplaire physique 2 de 2, contenu identique a wc009
# (voir ce fichier pour le detail des modeles et des arbitrages).


def GetAbilities() -> Sequence['Ability']:

    def magic_portal(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        initiator = effect.GetInitiator()
        this.RemoveThreatFromSchemes(effect.targets, 5, effect)

        icones = IconesBoostDuDessus(effect, initiator)
        if initiator is None:
            return

        if icones <= 1:
            initiator.DrawUp(1, effect)
        else:
            manigances = Worlds.GetOnFieldSchemes(effect)
            if manigances:
                this.RemoveThreatFromSchemes(manigances, 2, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            magic_portal,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
