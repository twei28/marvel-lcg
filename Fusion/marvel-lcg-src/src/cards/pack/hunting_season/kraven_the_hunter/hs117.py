from . import *

# hs117 / hs118 Predatory Ambush
# When Revealed : Kraven vous attaque ; en alter-ego, pas de carte de boost. Si un TRAP est attache a vous, distribue un piege.
# Boost : distribue un piege.

def GetAbilities() -> Sequence['Ability']:

    def embuscade(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        kraven = Kraven(effect)
        if kraven is not None:
            kraven.DoAttackYou(joueur, effect, property=AttackProperty(do_not_give_boost=joueur.IsAlterEgo()))
        if AUnPiegeAttache(effect, joueur):
            DonnerPiege(effect, joueur)

    def en_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        DonnerPiege(effect, message.GetToPlayer())

    return [
        AbilityFactory.WhenThisRevealed(None, embuscade),
        AbilityFactory.WhenCardBecomeBoost("This", en_boost),
    ]
