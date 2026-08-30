from . import *

# Precise Force (2/3) — exemplaire physique 2 de 3, contenu identique a
# ss004 (voir ce fichier pour le detail du modele repris).


def GetAbilities() -> Sequence['Ability']:

    def precise_force(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        value = initiator.DeclareNumber(0, 3)
        this.DealDamage(effect.targets, value, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            precise_force,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy)
        .SetName("Precise Force"),
    ]
