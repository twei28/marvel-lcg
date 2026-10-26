from . import *


def GetAbilities() -> Sequence['Ability']:
    def degat(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        Unused(message)
        effect.this.DealDamage(effect.targets, 1, effect)

    return [
        *AbilityFactory.GiveKeywordToAttached(CardFinder(name="Hogun"), attack=1, thwart=1),
        AbilityFactory.UnitAttackGainKeyword(
            "You",
            is_basic_attack=True,
            piercing=True,
            conditions=[lambda effect, message: nom_du_heros_actif(effect.this.GetControlByPlayer()) == "Hogun"],
        ),
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.HeroResponse,
            "You",
            degat,
            conditions=[lambda effect, message: message.trigger.IsName("Hogun")],
        ).SetTarget(Enemy),
    ]
