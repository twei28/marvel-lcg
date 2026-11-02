from . import *

# Psychic Control (OBLIGATION, x3 : hf610-hf612). Boost 3. « Forced Response : After your turn ends, Cassandra Nova schemes. Confuse your
# identity, then, discard this card. Alter-Ego Action : Exhaust your identity -> discard this card. »
# Cartes de reference : 32099 Warn the Others (`AfterPlayerTurnEnd(ForcedResponse, "AttachedPlayer")` + `PlayerActionToDiscardThis(AlterEgoAction)
# .SetCostFunc(CostFunc.Exhaust("YourIdentity"))`), hf120 (`villain.DoSchemes(joueur, effect)`).
# ⚠ « Cassandra Nova schemes » : contre le joueur qui porte l'obligation (le vilain manigance CONTRE lui, ce qui lui vaut aussi un compteur par le
# Forced Response du vilain) ; ordre imprime : manigance, puis desorientation, puis defausse.


def GetAbilities() -> Sequence['Ability']:
    def fin_de_tour(effect: 'Effect', message: 'Message.AfterPlayerTurnEnd') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = message.GetToPlayer()
        villain = VilainCN(effect)
        if villain is not None:
            villain.DoSchemes(joueur, effect)
        Faces.GiveStatus([joueur.GetIdentity()], "Confused", effect)
        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.AfterPlayerTurnEnd(AbilityType.ForcedResponse, "AttachedPlayer", fin_de_tour),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.AlterEgoAction).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
    ]
