from . import *
# * Captain Marvel (Monica Rambeau) — ALLIEE BASIQUE custom (jakxin), cout 3,
# [mental]. AERIAL. AVENGER. CTR 2 (1 conseq.) / ATQ 2 (1 conseq.), 3 PV.
# Interrupt: When Captain Marvel uses a basic power, spend 1 resource of any
#   type → search your discard pile for a card with a matching printed
#   resource and shuffle it into your deck.
#
# Modeles : `WhenUnitUseBasicPower(Interrupt, "This")` (friend.py:339),
# `CostFunc.Spend(Cost("1"))` dont `return_res` dit la couleur payee, ze014
# (`Search.PlayerCard(include_discard_pile=True, has_printed_res=...)`),
# `Faces.ShuffleAllTo(faces, joueur.player_deck, effect)`.
# ⚠ Un joker paye (`G`) correspond a une carte a joker IMPRIME : on lit la
#   couleur imprimee de la ressource depensee, sans conversion.

def GetAbilities() -> Sequence['Ability']:

    def captain_marvel(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        payee = effect.cost_func.Get(CostFunc.Spend).return_res
        for couleur in ("R", "B", "Y", "G"):
            if payee.GetColor(couleur, convert_green_res=False) > 0:
                face = Search.PlayerCard(effect, joueur, include_player_deck=False, include_discard_pile=True, has_printed_res=couleur)
                if face is not None:
                    Faces.ShuffleAllTo([face], joueur.player_deck, effect)
                return

    return [
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.Interrupt,
            "This",
            captain_marvel,
        ).SetCostFunc(CostFunc.Spend(Cost("1"))),
    ]
