from . import *

# Unbeatable!
# Hero Interrupt (defense): When Squirrel Girl defends against an attack, she
#   gets +2 DEF for that attack (+3 if you spent a Squirrel to play this card).
#   If that attack deals no damage to Squirrel Girl, ready Squirrel Girl.
#
# Meme montage que Desperate Defense (09015), qui est la carte de reference du
# pool pour ce texte.

def GetAbilities() -> Sequence['Ability']:

    def unbeatable(effect: 'Effect', message: 'Message.WhenUnitWouldDefend') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()
        message.GainDEFForThisAttack(3 if ADepenseUnEcureuil(effect) else 2, effect)

        message.IfYouTakeNoDamage(
            lambda: Faces.ReadyAll([initiator.GetHero()], effect)
        )

    return [
        AbilityFactory.WhenUnitDefendAgainstAttack(
            AbilityType.HeroInterrupt,
            "YourHero",
            unbeatable,
        ).SetPlay(),
    ]
