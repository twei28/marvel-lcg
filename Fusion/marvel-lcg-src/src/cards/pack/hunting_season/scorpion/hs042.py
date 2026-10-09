from . import *

# hs042 Human Fly

def GetAbilities() -> Sequence['Ability']:
    def prevenir(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        message.PreventDamage("All", effect)

    def en_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        carte = effect.this
        joueur = message.GetToPlayer()

        def donner() -> None:
            if joueur is not None and not carte.IsInPlay():
                joueur.DealEncounterCard(carte, effect)

        message.AfterThisActivation(effect, donner)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.ForcedInterrupt, "This", prevenir, is_from_attack=True,
        ).LimitOncePerRound(),
        AbilityFactory.WhenCardBecomeBoost("This", en_boost),
    ]
