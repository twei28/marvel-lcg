from . import *

# The Skrull Invasion 2B — complot principal, face B. Objectif 14[per_hero], escalade +X, menace de depart 1[per_hero].
# X is equal to twice the number of SKRULL enemies in play.
# Forced Response: After your turn ends, if there are less than 2[per_hero] suspicion counters on "Who Do You
#   Trust?", put a REVEALED minion at random from the IMPOSTOR deck into play engaged with you.
# If this stage is completed, the players lose the game.
#
# Cartes de reference : **`sk192b`** (meme squelette : `WhenCalcThisSchemeEscalation` + `AfterPlayerTurnEnd`),
# **`sk082b`..`sk085b`** (dernier stade : « If this stage is completed, the players lose the game » est la regle
# NATIVE du dernier complot, aucun script).
#
# ⚠ Mots-pieges : « TWICE the number of SKRULL ENEMIES » (mechant compris) ; X remplace une escalade imprimee :
# desc EscalationThreat « 0 » + escalade calculee ; « REVEALED minion » (pas un allie) ; « engaged with YOU » : le
# joueur dont le tour finit.


def GetAbilities() -> Sequence['Ability']:

    def escalade(effect: 'Effect') -> int:
        return 2 * len(EnnemisSkrull(effect))

    def fin_de_tour(effect: 'Effect', message: 'Message.AfterPlayerTurnEnd') -> None:
        if MoinsDeSoupcons(effect):
            MettreSbireRevele(effect, message.GetToPlayer())

    return [
        AbilityFactory.WhenCalcThisSchemeEscalation(escalade),
        AbilityFactory.AfterPlayerTurnEnd(AbilityType.ForcedResponse, "AnyPlayer", fin_de_tour),
    ]
