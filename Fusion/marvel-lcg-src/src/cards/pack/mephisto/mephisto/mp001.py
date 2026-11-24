from . import *

# Mephisto (I), stade 1. « [star] Devil's Pacts - Forced Interrupt : When Mephisto would activate against you, if you control a BARGAIN
# attachment, Mephisto does not activate and heals 1[per_hero] damage instead. If no damage was healed this way, place 1 threat on the main
# scheme for each BARGAIN attachment in play. » + mot-cle Steady (natif, `desc`).
# Cartes de reference : hf501b (villain, `WhenEnemyWouldActivate` « This » + `SetBeInstead`), dazzler/dz006 (filtre « against YOU » par
# `message.to_player`), shadowland/sl037. Le trait BARGAIN est lu sur les attachements de l'identite (`PactsDuJoueur`).


def GetAbilities() -> Sequence['Ability']:
    def pactes(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> None:
        PactsDuDiable(effect, message, 1)

    return [
        AbilityFactory.WhenEnemyWouldActivate(AbilityType.ForcedInterrupt, "This", pactes),
    ]
