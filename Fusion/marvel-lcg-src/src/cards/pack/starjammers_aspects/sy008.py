from . import *
# Steadfast Companions (Basic, evenement 2 [mental]). Team Up (Ch'od and Raza Longknife). Max 1 per deck.
# Action: Give Ch'od and Raza Longknife each a tough status card. Search your deck for an upgrade and add it to your hand.
#
# Cartes de reference : hc020 Green Hell / 12020 (`desc.TeamUp` + `SetTarget("TeamUp")`) ; `Faces.GiveStatus(cibles, "Tough", effect)` ;
# 08011 (`Search.PlayerCard`). « each a tough status card » : une carte Tenace PAR personnage ; un personnage deja Tenace n'en recoit pas
# une seconde (regle des statuts). « Search your DECK » : le deck seulement, pas la defausse.
def GetAbilities() -> Sequence['Ability']:
    def steadfast(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Faces.GiveStatus(effect.targets, "Tough", effect)
        joueur = effect.GetInitiator()
        face = Search.PlayerCard(effect, joueur, include_player_deck=True, include_discard_pile=False, card_type=Upgrade)
        if face:
            joueur.GainCard(face, effect)
    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            steadfast,
        ).SetPlay().SetTarget("TeamUp"),
    ]
