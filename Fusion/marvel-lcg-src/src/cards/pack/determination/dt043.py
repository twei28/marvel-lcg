from . import *

# * The Thing

def GetAbilities() -> Sequence['Ability']:

    # « Toughness » ne s'ecrit pas : le moteur lit le mot-cle dans le texte de la
    # carte (RegisterAttribute("Toughness", ...)). Luke Cage (01076) le porte et
    # n'a aucun module.
    def the_thing(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Ally)

        message.SetBeInstead(effect)
        this.CastTo(Unit2).TakeDamage(this, message.will_take_damage, effect)

    def check_votre_heros(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        this = effect.this.CastTo(Ally)
        player = this.GetControlByPlayer()
        if player is None:
            return False
        return message.trigger == player.GetHero()

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.ForcedInterrupt,
            None,
            the_thing,
            conditions=[check_votre_heros],
        ),
    ]
