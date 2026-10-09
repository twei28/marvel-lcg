from . import *

# Iguana Whip

def GetAbilities() -> Sequence['Ability']:

    def alter_ego(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        ThisCardGainSurge(effect)

    def heros(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        v = Vilain(effect)
        if v is None:
            return
        v.CastTo(Enemy).DoAttackYou(message.GetToPlayer(), effect)
        v = Vilain(effect)
        if v is None:
            return
        n = sum(1 for a in v.GetAttachedAttachments() if EstReptile(a))
        if n > 0:
            effect.this.PlaceThreatOnSchemes("MainScheme", n, effect)

    def menace(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        effect.this.PlaceThreatOnSchemes("MainScheme", 1, effect)

    return [
        AbilityFactory.WhenThisRevealed("Alter-Ego", alter_ego),
        AbilityFactory.WhenThisRevealed("Hero", heros),
        AbilityFactory.WhenCardBecomeBoost("This", menace, during_attack=True),
    ]
