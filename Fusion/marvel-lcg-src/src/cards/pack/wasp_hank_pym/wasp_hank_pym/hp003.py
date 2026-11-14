from . import *
# Gigantification — evenement. « Play only if you are in TINY hero form. »
# Hero Action (attack) : passe en GIANT, 4 degats a un ennemi en ignorant Guard.
# Hero Interrupt (defense) : quand un ennemi attaque, passe en GIANT et donne un statut Tough a ton heros.
def GetAbilities() -> Sequence['Ability']:
    def attaque(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        forme_vers(effect, "GIANT")
        this.DealDamage(effect.targets, 4, effect)
    def defense(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        forme_vers(effect, "GIANT")
        Faces.GiveStatus([effect.GetInitiator().GetIdentity()], "Tough", effect)
    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            attaque,
            conditions=[en_forme("TINY")],
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy)
        .SetIgnoreKeyword('Guard'),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.HeroInterrupt,
            Enemy,
            defense,
            conditions=[en_forme("TINY")],
        ).SetPlay().SetLabel('defense'),
    ]
