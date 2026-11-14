from . import *

# Hellfire Domination (side scheme 3[per_hero], icone Acceleration, boost 3). « When Defeated : Shuffle each set-aside Sebastian Shaw encounter card
# into the encounter deck. » Cartes de reference : 04141 (`WhenSchemeBeDefeated`), `Faces.ShuffleAllTo(faces, "EncounterDeck", effect)` (hf-fondations
# campaign.py), `Worlds.GetSetAsideAreaCards(effect, CardFinder(...))`.
# ⚠ « each set-aside Sebastian Shaw encounter CARD » : toute carte du set « Sebastian Shaw » de la zone mise de cote (pas seulement les attachements).


def GetAbilities() -> Sequence['Ability']:
    def vaincue(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        cartes = [f for f in Worlds.GetSetAsideAreaCards(effect) if f.paper.set_name == SET_SHAW]
        if cartes:
            Faces.ShuffleAllTo(cartes, "EncounterDeck", effect)

    return [AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincue)]
