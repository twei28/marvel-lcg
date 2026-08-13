from . import *

# * Starling

def GetAbilities() -> Sequence['Ability']:

    def starling(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        this = effect.this.CastTo(Ally)

        player = this.GetControlByPlayer()
        if player is None:
            return
        # « jusqu'a la fin de la PARTIE » : un gain DURABLE, pose une fois et
        # jamais repris — c'est `Gain` (precedent mw023.py:25). Les
        # `GainUntil...End` du moteur expirent tous trop tot.
        player.GetHero().Gain(effect, 1, attack=1)

    return [
        Fragile(),
        AbilityFactory.AfterUnitTookDamage(
            AbilityType.HeroResponse,
            "This",
            starling,
            is_from_attack=True,
            conditions=[lambda effect, message: message.took_damage >= 5],
        ),
    ]
