from . import *

# * Starling

def GetAbilities() -> Sequence['Ability']:

    def starling(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        this = effect.this.CastTo(Ally)

        player = this.GetControlByPlayer()
        if player is None:
            return
        # « jusqu'a la fin de la PARTIE » : le moteur n'a pas de duree pareille
        # pour un gain temporaire. Un gain permanent pose sur le heros est ce
        # qui s'en approche — il disparait avec lui, pas avant.
        player.GetHero().GainKeywordPermanently(effect, attack=1)

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
