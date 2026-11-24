from . import *

# Claustrophobia
#
# ERRATA RRG 1.7 / 1.8 (Annexe V, Storm Hero Pack #30) : « You cannot change to HERO form » (au lieu de « change forms »).
#   Equivalent en pratique : a la revelation le joueur est force en alter-ego, donc seul le passage au heros reste possible ; `PlayersCannotChangeForms` l'interdit.
#   Cas : `36030` de `tools/cas/errata_rrg.py`. Relu le 03/11/2026 : rien a changer.

def GetAbilities() -> Sequence['Ability']:

    def claustrophobia(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Obligation)
        player = this.GetGaveToPlayer()

        identity = player.GetIdentity()
        identity.ChangeToForm(AlterEgo, effect)


    return [
        AbilityFactory.WhenThisRevealed(
            None,
            claustrophobia
        ),
        AbilityFactory.PlayersCannotChangeForms(
            AbilityType.NonKeyword,
            "AttachedPlayer"
        ),
        AbilityFactory.PlayerActionToRemoveThisFromGame(
            AbilityType.AlterEgoAction
        ).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
    ]

