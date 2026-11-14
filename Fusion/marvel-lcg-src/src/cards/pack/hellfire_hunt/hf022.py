from . import *

# * Sage (Tessa) : allie RECRUITED, cout 1, PV 3, THW 1*, ATK 1*. [star] Response.
# Response: After Sage thwarts, discard the top card of the encounter deck. Stun a minion if that card has a star icon in the boost area.
#
# Cartes de reference : 01159 Ritual Combat (`Worlds.DiscardEncounterCards(1, effect)` + `FacesCounter.CountTotalBoostIcons`),
# `FacesCounter.CountTotalBoostStar` (faces_counter.py:152), `AfterUnitMakeThwart` (thwart.py).
# ⚠ « a minion » : un sbire AU CHOIX (n'importe lequel en jeu), pas seulement un sbire engage.
def GetAbilities() -> Sequence['Ability']:
    def sage(effect: 'Effect', message: 'Message.AfterUnitThwartEnd') -> None:
        faces = Worlds.DiscardEncounterCards(1, effect)
        if FacesCounter.CountTotalBoostStar(faces) > 0:
            Faces.GiveStatus(effect.targets, "Stunned", effect)

    return [
        AbilityFactory.AfterUnitMakeThwart(
            AbilityType.Response,
            "This",
            sage,
        ).SetTarget(Minion, canbe_stunned=True, is_optional=True),
    ]
