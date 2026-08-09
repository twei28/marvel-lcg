from . import *

# Order of the Web — custom « Kajislav », carte d'aspect LEADERSHIP
# Play under any player's control. Max 1 TEAM card per player.
# Action: Exhaust Order of the Web -> choose an ally with "Spider" in its title
#   in your discard pile and shuffle it into your deck.
#
# La limite « Max 1 TEAM card per player » reste TEXTUELLE : Mighty Avengers
# (21015), qui porte exactement la meme phrase et le meme trait TEAM, n'a
# aucune cle `desc` pour cela et aucun script. Le moteur ne l'applique donc pas
# — et surtout pas via `MaxPerUnit`, qui veut dire « 1 exemplaire par
# personnage » et ne concerne que les ameliorations.

def GetAbilities() -> Sequence['Ability']:

    def a_spider_dans_le_titre(effect: 'Effect', face: 'CardFace') -> bool:
        return "Spider" in face.name

    def ordre_de_la_toile(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        initiator = effect.GetInitiator()
        Faces.ShuffleAllTo(effect.targets, initiator.player_deck, effect)

    return [
        AbilityFactory.CanPlayThisSupportCard(
            under_any_players_control=True
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            ordre_de_la_toile
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Ally, check_fn=a_spider_dans_le_titre, from_where=["YourDiscardPile"]),
    ]
