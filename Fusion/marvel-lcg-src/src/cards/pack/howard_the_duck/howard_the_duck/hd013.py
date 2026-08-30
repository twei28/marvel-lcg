from . import *

# * Beverly Switzler — PERSONA — soutien, cout 1
# Alter-Ego Action: Exhaust Beverly Switzler → return the bottommost Howard
#   the Duck card from your discard pile to your hand. Heal 1 damage from your
#   identity.
#
# Structure : modele ok011 (Upanga), meme
# `AbilityFactory.WhenInYourPlayTurn(AbilityType.AlterEgoAction, ...)` +
# `.SetCostFunc(CostFunc.Exhaust("This"))`.
#
# « the BOTTOMMOST Howard the Duck card » : le moteur a bien une cible
# `from_where=["YourDiscardPileBottommost"]` (il009 Vision AI), mais elle ne
# prend QUE la carte du fond, sans filtre de set — inutilisable ici, ou il
# faut la plus basse PARMI les cartes du set « Howard the Duck ». La
# recherche est donc faite a la main sur `player.discard_pile.Get()`, qui rend
# la defausse du FOND vers le dessus (`Deck.GetAll(from_top=False)`,
# deck.py:381-387 ; c'est exactement ce que consulte
# `get_YourDiscardPileBottommost`, selector_where.py:114) : le premier
# element filtre est donc le bon.
# Le filtre est le SET, pas le trait ni le nom : « a Howard the Duck card »
# designe une carte de son kit signature (set_name « Howard the Duck »), pas
# les cartes de son set nemesis, qui ne peuvent de toute facon pas se trouver
# dans la defausse d'un joueur.
#
# Retour en main : `Faces.ReturnToHand` (modele il009). Soin :
# `this.HealthUnits([identite], 1, effect)` (modele il002 Stature).


def GetAbilities() -> Sequence['Ability']:

    def beverly_switzler(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        finder = CardFinder(set_name=SET_HOWARD)
        candidates = [f for f in initiator.discard_pile.Get() if finder.Check(f)]
        if candidates:
            Faces.ReturnToHand([candidates[0]], initiator, effect)

        this.HealthUnits([initiator.GetIdentity()], 1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            beverly_switzler,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
