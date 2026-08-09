from . import *

# Radiate — custom « DesignHacker » (coût X)
# Choose one:
# - Hero Action (attack): Place 2 flame counters on X enemies.
# - Action: Remove all flame counters from X enemies -> change your form,
#   then heal 1 damage for each flame counter removed this way (to a maximum
#   of 5).

def GetAbilities() -> Sequence['Ability']:

    def placer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        cibles = effect.targets[:effect.GetCostX()]
        Faces.PlaceCountersOn(cibles, 2, 'flame', effect)

    def retirer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        cibles = effect.targets[:effect.GetCostX()]
        retires = Faces.RemoveCountersOn(cibles, "All", 'flame', effect) or 0

        initiator = effect.GetInitiator()
        identity = initiator.GetIdentity()
        identity.ChangeToForm(AlterEgo if initiator.IsHero() else Hero, effect)

        soin = min(retires, 5)
        if soin > 0:
            this.HealthUnits([initiator.GetIdentity()], soin, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            placer
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy, range=(1, "All")),

        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            retirer
        ).SetPlay()
        .SetTarget(CardFinder(card_type=Enemy, has_counter='flame'), range=(1, "All")),
    ]
