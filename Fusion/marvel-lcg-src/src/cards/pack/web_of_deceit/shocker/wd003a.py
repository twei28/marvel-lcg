from . import *

# Look Who Finally Showed (2A)

def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # « Search the encounter deck and discard pile for the Rhino minion and
        # put him into play engaged with the first player. »
        #
        # Rhino n'est PAS du set Shocker : il vient de City in Chaos, le
        # modulaire officiel que le livret impose a ce scenario.
        premier = Worlds.GetFirstPlayer(effect)
        rhino = Search.SearchForCard(
            effect,
            premier,
            include_encounter_deck=True,
            include_encounter_discard_pile=True,
            name="Rhino",
        )
        if rhino:
            rhino.PutIntoPlay(premier, effect)
        ChercherEtReveler(effect, name="Grand Larceny")

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
    ]
