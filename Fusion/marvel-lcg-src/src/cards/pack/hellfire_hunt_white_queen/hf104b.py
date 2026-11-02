from . import *

# Infiltrating the Mansion (1B), stade 1. « When Completed : Flip White Queen and place 1 acceleration token here. » ;
# « Forced Response : After the round ends, advance to stage 2A. »
# Cartes de reference : gs118b / sk145b (`WhenMainSchemeStageCompleted`), `CanAccelerationToken.PlaceAccelerationToken` (les jetons
# d'acceleration d'un complot passent au stade suivant : `AdvanceMainScheme`, « Fix 32127b »), tk001a (retournement).
# ⚠ LECTURE (QUESTIONS.md n°1) : le stade se TERMINE donc de deux facons : (a) la menace atteint le seuil (2 par heros) : « When
# Completed » puis le moteur avance tout de suite ; (b) sinon, a la fin du round, la Reponse forcee le fait avancer. Le stade 1 dure ainsi
# AU PLUS un round, ce que la carte imprime.


def GetAbilities() -> Sequence['Ability']:
    def terminee(effect: 'Effect', message: 'Message.WhenMainSchemeStageCompleted') -> None:
        this = effect.this.CastTo(MainScheme)
        RetournerWQ(effect)
        this.PlaceAccelerationToken(1, effect)

    def fin_de_round(effect: 'Effect', message: 'Message.AfterRoundEnd') -> None:
        this = effect.this.CastTo(MainScheme)
        if this.IsInPlay():
            this.Advance("2A", effect)

    return [
        AbilityFactory.WhenMainSchemeStageCompleted(AbilityType.ForcedInterrupt, "This", terminee),
        AbilityFactory.AfterRoundEnd(AbilityType.ForcedResponse, fin_de_round),
    ]
