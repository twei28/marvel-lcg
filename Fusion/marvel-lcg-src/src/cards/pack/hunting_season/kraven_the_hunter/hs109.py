from . import *

# hs109 * Last Son of Kraven
# Forced Interrupt : quand un personnage que vous controlez l'attaque, distribue un piege (limite 1 par ronde, tous joueurs confondus).
# Boost : apres l'activation, le melanger dans le paquet de rencontre.

def GetAbilities() -> Sequence['Ability']:

    def distribuer(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        DonnerPiege(effect, message.attacker.GetControlByPlayer())

    return [
        AbilityFactory.WhenUnitWouldBeAttacked(AbilityType.ForcedInterrupt, "This", distribuer).LimitOncePerRound(),
        AbilityFactory.WhenBoostShuffleThisIntoEncounterDeckAfterActivationEnd(),
    ]
