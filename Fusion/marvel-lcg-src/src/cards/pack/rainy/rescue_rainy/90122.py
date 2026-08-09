from . import *

# Magnetic Deflector

def GetAbilities() -> Sequence['Ability']:

    def limite_deux_par_round(effect: 'Effect', message: 'Message2') -> bool:
        """« Limit twice per round » : le moteur n'offre que la limite a 1.

        `world.stat.once_per_round_effects` enregistre TOUS les effets resolus
        depuis le debut du round, on y compte donc nos propres declenchements.
        """
        deja = [x for x in effect.world.stat.once_per_round_effects
                if x.ability is effect.ability]
        return len(deja) < 2

    def deflecteur(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        message.GainATKForThisAttack(-1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.HeroInterrupt,
            Enemy,
            deflecteur,
            conditions=[limite_deux_par_round],
        ).SetLabel('defense')
        # Le cout est la defausse de la carte du dessus de son deck.
        .SetCostFunc(CostFunc.DiscardDeckTopCards("YourDeck", 1)),
    ]
