from . import *

# hs162 * King Cobra
# Engage avec vous, votre heros ne peut pas attaquer d'autres ennemis. Boost : si cette attaque vous blesse, epuisez
# votre identite.

def GetAbilities() -> Sequence['Ability']:

    def heros_engage(effect: 'Effect', message: 'Message.CheckIfUnitCanBeAttackBy') -> bool:
        joueur = effect.this.CastTo(Minion).engaged_player
        return joueur is not None and message.attacker is joueur.GetHero()

    def epuiser(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        joueur = message.trigger.GetControlByPlayer()
        Faces.ExhaustAll([joueur.GetIdentity()], effect)

    return [
        *AbilityFactory.UnitCannotAttackTarget(Hero, can_only_attack="This", conditions=[heros_engage]),
        AbilityFactory.BoostIfThisActivationDealsDamage("You", epuiser),
    ]
