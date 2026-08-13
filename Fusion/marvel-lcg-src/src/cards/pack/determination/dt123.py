from . import *

# * Ralph

def GetAbilities() -> Sequence['Ability']:

    def ralph(effect: 'Effect', message: 'Message.WhenUnitWouldAttackUnit') -> None:
        this = effect.this.CastTo(Ally)

        initiator = effect.GetInitiator()
        ennemi = message.target
        this.AttachTo2(ennemi, effect)

        faces = list(initiator.LookAtDeck("EncounterDeck", 1, effect))
        faces += list(initiator.dealt_encounter_cards.Get())[:1]
        x = sum(f.CastTo(HasBoostIcon).boost_icon for f in faces)
        if x <= 0:
            return
        message.GainPiercing(effect)
        this.DealDamage([ennemi], x, effect)
        this.DealDamage([this], x, effect)

    return [
        AbilityFactory.WhenUnitWouldAttackUnit(
            AbilityType.HeroInterrupt,
            "You",
            Enemy,
            ralph,
        ),
    ]
