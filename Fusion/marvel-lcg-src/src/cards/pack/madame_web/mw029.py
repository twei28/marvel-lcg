from . import *

# Female Power — custom « Kajislav », carte d'aspect LEADERSHIP
# Hero Action (attack): Deal 2 damage to an enemy for each character with
#   "Girl", "Lady", "Madame", "Ms.", "She", or "Woman" in its title you control.

MOTS = ("Girl", "Lady", "Madame", "Ms.", "She", "Woman")


def GetAbilities() -> Sequence['Ability']:

    def pouvoir_feminin(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        initiator = effect.GetInitiator()
        nombre = 0
        for face in initiator.GetControlCharacters():
            if any(mot in face.name for mot in MOTS):
                nombre += 1

        if nombre > 0:
            this.DealDamage(effect.targets, 2 * nombre, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            pouvoir_feminin
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
