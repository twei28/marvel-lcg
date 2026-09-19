from . import *

# Maggia Underboss (Villainous : base automatique)
# [star] Forced Interrupt: When Maggia Underboss activates against you, if you
#   are stunned, give it an additional boost card for this activation.
#
# Modele : 02020 Hysteria (WhenUnitWouldAttack + WhenUnitWouldScheme, meme
# handler, GiveAdditionalBoostCardForThisActivation). « you are stunned » = ton
# identite porte le statut, teste dans `conditions` (un filtre ne va jamais
# dans le corps, RECETTES §1).

def GetAbilities() -> Sequence['Ability']:

    def joueur_etourdi(effect: 'Effect', message: 'Message.WhenUnitWouldAttack|Message.WhenUnitWouldScheme') -> bool:
        joueur = message.GetAgainstPlayer()
        return joueur is not None and joueur.GetIdentity().IsStunned()

    def boost_en_plus(effect: 'Effect', message: 'Message.WhenUnitWouldAttack|Message.WhenUnitWouldScheme') -> None:
        message.GiveAdditionalBoostCardForThisActivation(1, effect)

    return [
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.ForcedInterrupt,
            "This",
            boost_en_plus,
            conditions=[joueur_etourdi],
        ),
        AbilityFactory.WhenUnitWouldScheme(
            AbilityType.ForcedInterrupt,
            "This",
            boost_en_plus,
            conditions=[joueur_etourdi],
        ),
    ]
