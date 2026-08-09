from . import *

# * Silk (Cindy Moon) — alliee signature, custom « Rainy »
# Action: Return Silk to your reserve → stun a minion and deal 2 damage to it.
# Response: After you play Silk from your hand, search the encounter deck for a
#   treachery and discard it.
#
# La Response dit « from your HAND » et l'insert le confirme noir sur blanc :
#   « Q: Does Silk get to discard a treachery after I play her from my reserve?
#     A: No. Your reserve is not your hand. »
# D'ou `EstJoueeDepuisLaMain` : `is_like_from_hand` serait vrai depuis la
# reserve aussi, puisque la reserve est precisement une zone « comme la main ».

def GetAbilities() -> Sequence['Ability']:

    def retour_en_reserve(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)

        # Le retour en reserve est le COUT de l'action (`CostFunc.ReturnToReserve`
        # ci-dessous) : quand on arrive ici, Silk est deja en reserve.
        cibles = effect.targets
        if cibles:
            Faces.GiveStatus(cibles, "Stunned", effect)
            this.DealDamage(cibles, 2, effect)

    def chercher_une_traitrise(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        joueur = message.GetToPlayer()
        trouvee = Search.EncounterCard(
            effect,
            joueur,
            include_discard_pile=False,
            card_type=Treachery,
        )
        if trouvee is not None:
            Faces.DiscardAll([trouvee], effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            retour_en_reserve,
        ).SetTarget(Minion)
        .SetCostFunc(CostFunc.ReturnToReserve("This")),

        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Response,
            "You",
            "This",
            chercher_une_traitrise,
            conditions=[EstJoueeDepuisLaMain],
        ),
    ]
