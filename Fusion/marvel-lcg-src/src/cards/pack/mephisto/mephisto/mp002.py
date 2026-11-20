from . import *

# Mephisto (II), stade 2. + « When Revealed : Find and attach the Hell Lord attachment to Mephisto » (`AttacherLeHellLord`, modele `AttacherUnePoigne` de kree_sentry). « [star] Devil's Pacts - Forced Interrupt : When Mephisto would activate against you, if you control a BARGAIN
# attachment, Mephisto does not activate and heals 2[per_hero] damage instead. If no damage was healed this way, place 1 threat on the main
# scheme for each BARGAIN attachment in play. » + mot-cle Steady (natif, `desc`).
# Cartes de reference : hf501b (villain, `WhenEnemyWouldActivate` « This » + `SetBeInstead`), dazzler/dz006 (filtre « against YOU » par
# `message.to_player`), shadowland/sl037. Le trait BARGAIN est lu sur les attachements de l'identite (`PactsDuJoueur`).


def GetAbilities() -> Sequence['Ability']:
    def pactes(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> None:
        PactsDuDiable(effect, message, 2)

    def hell_lord(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        AttacherLeHellLord(effect, effect.this)

    return [
        AbilityFactory.WhenEnemyWouldActivate(AbilityType.ForcedInterrupt, "This", pactes),
        AbilityFactory.WhenThisRevealed(None, hell_lord),
    ]
