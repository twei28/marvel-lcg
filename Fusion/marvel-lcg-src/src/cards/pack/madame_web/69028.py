from . import *

# Advice — custom « Kajislav », carte d'aspect LEADERSHIP
# Action: Choose an ally and discard the top card of the encounter deck. That
#   ally gets +X ATK this phase, where X is equal to the number of boost icons
#   ([boost]) discarded this way.

def GetAbilities() -> Sequence['Ability']:

    def conseil(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        faces = Worlds.DiscardEncounterCards(1, effect)
        valeur = FacesCounter.CountTotalBoostIcons(faces)
        if valeur <= 0:
            return

        for target in effect.targets:
            target.GainUntilPhaseEnd(effect, attack=valeur)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            conseil
        ).SetPlay()
        .SetTarget(Ally),
    ]
