from . import *

# Excessive Force

def GetAbilities() -> Sequence['Ability']:

    def excessive_force(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        initiator = effect.GetInitiator()
        # X est le cout paye : une carte a cout variable se lit dans ce qui a
        # ete depense pour elle.
        paid = getattr(effect.context, 'paid_this_resources', None)
        valeur = paid.val if paid else 0

        cible = effect.targets[0] if effect.targets else None
        avait_tough = bool(cible and cible.CastTo(CanStatus).HasStatus("Tough"))

        this.DealDamage(effect.targets, valeur, effect,
                        property=AttackProperty(piercing=True))

        if cible is not None and cible.CastTo(Unit2).IsDefeated():
            initiator.DrawUp(valeur, effect)
        if avait_tough and cible is not None \
                and not cible.CastTo(CanStatus).HasStatus("Tough"):
            initiator.DrawUp(2, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            excessive_force
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
