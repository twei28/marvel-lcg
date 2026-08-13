from . import *

# * Quasar

def GetAbilities() -> Sequence['Ability']:

    def quasar(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)

        initiator = effect.GetInitiator()
        # « chaque ennemi engage avec vous » : le vilain en fait partie quand il
        # est engage, d'ou Enemy et pas YourEngagedMinions (ra005 fait de meme).
        engages = Worlds.FindCardsOnField(
            effect,
            card_type=Enemy,
            engaged_with=initiator,
        )
        engages = [x for x in engages if not x.IsDefeated()]
        if engages:
            this.DealDamage(engages, 2, effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            quasar
        ),
    ]
