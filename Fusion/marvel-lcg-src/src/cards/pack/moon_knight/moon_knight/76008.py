from . import *

# Fight or Foil — custom « DesignHacker »
# Choose one:
# - Action (attack): Change form to Moon Knight -> deal 2 damage to an enemy.
# - Action (thwart): Change form to Mr. Knight -> remove 2 threat from a scheme.
# Deux capacités Play distinctes : le moteur propose le choix au moment de
# jouer la carte (modèle Wasp Sting 13006 / Radiate 64009).


def GetAbilities() -> Sequence['Ability']:

    def branche_attaque(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        initiator = effect.GetInitiator()
        ChangerVersFaceNommee(initiator, effect, "Moon Knight")
        this.DealDamage(effect.targets, 2, effect)

    def branche_contre(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        initiator = effect.GetInitiator()
        Unused(initiator)
        ChangerVersFaceNommee(effect.GetInitiator(), effect, "Mr. Knight")
        this.RemoveThreatFromSchemes(list(effect.targets), 2, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            branche_attaque,
            conditions=[
                lambda effect, message:
                    TrouverFaceIdentite(effect.GetInitiator(), "Moon Knight") is not None,
            ],
        ).SetPlay()
        .SetLabel('attack')
        .SetTarget(Enemy),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            branche_contre,
            conditions=[
                lambda effect, message:
                    TrouverFaceIdentite(effect.GetInitiator(), "Mr. Knight") is not None,
            ],
        ).SetPlay()
        .SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
