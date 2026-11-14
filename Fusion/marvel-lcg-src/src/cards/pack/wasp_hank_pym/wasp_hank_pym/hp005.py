from . import *
# Self-Shrinking — evenement. « Play only if you are in GIANT hero form. »
# Hero Action (thwart) : passe en TINY, retire 3 menaces d'une manigance en ignorant Patrol.
# Hero Interrupt (defense) : quand un ennemi declare une attaque contre toi, passe en TINY et annule cette attaque.
def GetAbilities() -> Sequence['Ability']:
    def menee(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        forme_vers(effect, "TINY")
        this.RemoveThreatFromSchemes(effect.targets, 3, effect)
    def defense(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        forme_vers(effect, "TINY")
        message.CancelThisAttack(effect)
    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            menee,
            conditions=[en_forme("GIANT")],
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2)
        .SetIgnoreKeyword('Patrol'),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.HeroInterrupt,
            Enemy,
            defense,
            against_player="You",
            conditions=[en_forme("GIANT")],
        ).SetPlay().SetLabel('defense'),
    ]
