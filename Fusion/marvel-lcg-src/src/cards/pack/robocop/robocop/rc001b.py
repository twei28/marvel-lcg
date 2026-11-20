from . import *

# * Alex Murphy (face alter-ego) : REC 3, main 5, PV 14. CYBORG. OFFICER.
# You may include up to 6 Justice cards in your deck during deck-building.
# Action: Exhaust Alex Murphy → search your deck for an identity-specific upgrade and add it to your hand.
#
# CARTES DE REFERENCE
#  - `ok001b` / `an001b` : `Search.PlayerCard(include_player_deck=True, ..)` + `GainCard`. `ar003` : `card_class="IdentitySpecific"` pour « identity-specific ».
#  - `CostFunc.Exhaust("YourIdentity")` (`ar010`, `mf013`) : l'alter-ego s'incline lui-meme.
#
# TEXTE CONTRE CODE
#  « up to 6 Justice cards in your deck » : regle de CONSTRUCTION de deck, sans effet en partie (comme les autres « you may include » du depot).
#  « search your DECK » -> le deck du joueur seul (pas la defausse). « an identity-specific UPGRADE » -> classe IdentitySpecific ET type amelioration.
#  Action nue (`AbilityType.Action`), sans limite imprimee. Aucun melange imprime : le deck n'est pas melange.
#  Chiffres : REC 3, main 5, PV 14.


def GetAbilities() -> Sequence['Ability']:

    def alex_murphy(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        face = Search.PlayerCard(
            effect,
            joueur,
            include_player_deck=True,
            card_type=Upgrade,
            card_class="IdentitySpecific",
        )
        if face:
            joueur.GainCard(face, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            alex_murphy,
        ).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
    ]
