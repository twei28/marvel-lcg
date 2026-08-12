from . import *

# Symbiotic Fury — custom « Rainy »
# Hero Response: After you take damage, take 1 additional damage -> ready
#   your hero. Then, if you have sustained 6 or more total damage, deal 2
#   damage to an enemy.

def GetAbilities() -> Sequence['Ability']:

    def symbiotic_fury(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        this = effect.this.CastTo(Event)

        initiator = effect.GetInitiator()
        identity = initiator.GetIdentity()

        identity.TakeDamage(this, 1, effect)
        Faces.ReadyAll([identity], effect)

        if identity.max_health - identity.health >= 6:
            ennemis = list(Worlds.FindCardsOnField(effect, card_type=Enemy))
            if ennemis:
                initiator.ChooseAbilities(
                    effect,
                    AbilityFactory.ForChoiceAbility(
                        "Deal 2 damage to an enemy",
                        lambda targets: this.DealDamage(list(targets), 2, effect),
                    ).SetTarget(Select.From(faces=ennemis), range=(1, 1)),
                )

    return [
        AbilityFactory.AfterUnitTookDamage(
            AbilityType.HeroResponse,
            "You",
            symbiotic_fury,
        ).SetPlay(hero_form_only=True),
    ]
