from . import *

# Silent Takeover (2A). « When Revealed : Each player finds their own nemesis minion and put it into play engaged with themself. »
# Cartes de reference : hf321 Echoes of Enmity (`Search.EncounterCard(..., card_type=Minion, is_nemesis=joueur)`), `Card.PutIntoPlay(joueur)`.
# ⚠ « finds » : deck, defausse ET zone de cote (le set nemesis est « mis de cote » a la mise en place) ; sans sbire nemesis, rien.


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        for joueur in Worlds.GetPlayers(effect):
            sbire = Search.EncounterCard(effect, joueur, include_discard_pile=True, include_set_aside=True, card_type=Minion, is_nemesis=joueur)
            if sbire is not None:
                sbire.PutIntoPlay(joueur, effect)

    return [AbilityFactory.WhenThisRevealed(None, revelee)]
