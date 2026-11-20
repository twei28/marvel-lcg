from . import *
# Remise. Evenement ATTACK SKILL, cout 1.
#
# Hero Action (attack): Deal 3 damage to an enemy. If the last card you played was Riposte, ready Corsair.
#
# Cartes de reference : 01021 Gamma Slam (`WhenInYourPlayTurn(HeroAction).SetPlay().SetLabel('attack').SetTarget(Enemy)`
# + `DealDamage`), nt005 Kickflip (la derniere carte jouee), 01024 One-Two Punch (redresser le heros).
def GetAbilities() -> Sequence['Ability']:
    def remise(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        joueur = JoueurDe(effect)
        this.DealDamage(effect.targets, 3, effect)
        if joueur is not None and DerniereEstUne(effect, joueur, RIPOSTE):
            Faces.ReadyAll([joueur.GetIdentity()], effect)
    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            remise,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
