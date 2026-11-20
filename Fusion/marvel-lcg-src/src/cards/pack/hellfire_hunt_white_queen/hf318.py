from . import *

# Hellfire Hunt. Manigance annexe, icone Hazard. « Each HELLFIRE minion gets +1 ATK. When Revealed : Each player searches the encounter deck and
# discard pile for a HELLFIRE minion and puts it into play engaged with them. » Cartes de reference : 01136 Ultron (`GiveKeywordToInPlayWhenApplyThis(...,
# attack=1)`), masters_of_mayhem 01133 (`Search.EncounterCard` + `PutIntoPlay`).


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        for joueur in Worlds.GetPlayers(effect):
            face = Search.EncounterCard(effect, joueur, include_discard_pile=True, trait="HELLFIRE", card_type=Minion)
            if face is not None:
                face.PutIntoPlay(joueur, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder2("HELLFIRE", Minion), attack=1),
        AbilityFactory.WhenThisRevealed(None, revelee),
    ]
