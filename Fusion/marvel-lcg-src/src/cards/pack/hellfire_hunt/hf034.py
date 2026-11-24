from . import *

# Xavier's School Under Siege (POTENTIAL ALLY, Glob Herman). Victory 1.
# When Revealed: The first player searches the encounter deck and discard pile for a minion and puts it into play engaged with them.
# When Defeated : Glob Herman.
#
# Cartes de reference : 54007 Safe House #30 (`Search.EncounterCard` + `face.PutIntoPlay(joueur, effect)` qui engage le sbire),
# `world.GetFirstPlayer()`. ⚠ « encounter deck AND DISCARD PILE » : `include_discard_pile=True` (54007 ne fouille pas la defausse).
def GetAbilities() -> Sequence['Ability']:
    def ecole(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        premier = effect.world.GetFirstPlayer()
        face = Search.EncounterCard(
            effect,
            premier,
            include_discard_pile=True,
            card_type=Minion,
        )
        if face:
            face.PutIntoPlay(premier, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, ecole),
        AbilitePotentialAlly("Glob Herman"),
    ]
