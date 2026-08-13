from . import *

# The Check Cleared

def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        # « Place threat on The Long Night equal to the combined SCH of each
        # CRIMINAL enemy in play. »
        total = 0
        for face in Worlds.GetOnFieldCards(effect):
            if Enemy.IsType(face) and face.HasTrait("CRIMINAL"):
                total += face.CastTo(HasScheme).scheme
        nuit = Worlds.FindCardOnField(effect, name="The Long Night")
        if nuit and total > 0:
            this.PlaceThreatOnSchemes([nuit], total, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
    ]
