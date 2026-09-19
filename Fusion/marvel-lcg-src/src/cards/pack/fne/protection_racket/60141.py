from . import *

# Change of Venue — Surge : base desc.
# When Revealed: Swap your main scheme with a random set-aside main scheme.
#   Place the threat from the previous scheme on the new scheme.
# [star] Boost: Resolve this card's "When Revealed" ability.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        EchangerLeComplot(effect, message.GetToPlayer())

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        EchangerLeComplot(effect, message.GetToPlayer())

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
