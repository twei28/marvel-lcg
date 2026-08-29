from . import *

# * Stature (Cassie Lang)
# Response: After Stature enters play, heal 1 damage from your identity.
#   You may discard up to 3 cards from your deck to heal 1 more damage for
#   each card discarded.
#
# Modele du declencheur : ok003 Ayo (okoye/okoye/ok003.py),
# `AbilityFactory.AfterCardEnterPlay(AbilityType.Response, "This", ...)`.
# Le montant variable se demande via `initiator.DeclareNumber(0, 3)` (comme
# Aerial Intervention, angel/42014.py) puis se defausse via
# `DiscardDeckTopCards` (pas de choix de carte precise dans le texte
# imprime -- les N premieres du dessus, convention par defaut du moteur).

def GetAbilities() -> Sequence['Ability']:

    def stature(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)

        initiator = effect.GetInitiator()
        identity = initiator.GetIdentity()

        n = initiator.DeclareNumber(0, 3)
        discarded = initiator.DiscardDeckTopCards(n, effect) if n else []

        this.HealthUnits([identity], 1 + len(discarded), effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            stature,
        ),
    ]
