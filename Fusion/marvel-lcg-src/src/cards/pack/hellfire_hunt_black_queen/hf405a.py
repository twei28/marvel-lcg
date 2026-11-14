from . import *

# The Power of the Darkhold (2A). « When Revealed : Shuffle the set-aside Darkhold modular set into the encounter deck. »
# Cartes de reference : skrull_menace/shaper_of_worlds (`Worlds.GetSetAsideAreaCards`), `Faces.ShuffleAllTo(faces, "EncounterDeck")`.
# ⚠ La zone « mise de cote » contient AUSSI les allies Recruited de campagne : on filtre sur le NOM DU SET (`paper.set_name == "Darkhold"`).


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        faces = [f for f in Worlds.GetSetAsideAreaCards(effect) if f.paper.set_name == ENSEMBLE_DARKHOLD]
        if faces:
            Faces.ShuffleAllTo(faces, "EncounterDeck", effect)

    return [AbilityFactory.WhenThisRevealed(None, revelee)]
