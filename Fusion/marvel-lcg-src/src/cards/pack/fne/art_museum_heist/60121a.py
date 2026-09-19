from . import *
from cards.pack.fne.campaign import CapacitesDeCampagne

# Art Museum Heist (1A)
# Setup: Find this encounter set's 4 ART attachments and attach 1 at random to
#   the villain. Shuffle the other 3 into the encounter deck.
#
# Les 4 oeuvres sont mises de cote par le scenario (set_aside). Modele : 55004a
# Prime Real Estate (SetupCards.AttachTo choose="Random", include_in_play=False),
# puis Faces.ShuffleAllTo(..., "EncounterDeck") pour les trois autres.

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        vilain = Worlds.FindVillain(effect)
        if vilain is None:
            return
        SetupCards.AttachTo(
            effect,
            attach_to=vilain,
            finder=CardFinder(trait="ART", card_type=Attachment),
            include_in_play=False,
            choose="Random",
        )
        restantes = Worlds.GetSetAsideAreaCards(effect, CardFinder(trait="ART", card_type=Attachment))
        if restantes:
            Faces.ShuffleAllTo(restantes, "EncounterDeck", effect)

    return [
        AbilityFactory.WhenCardSetup(
            "This",
            mise_en_place,
        ),
        *CapacitesDeCampagne("art_museum_heist"),
    ]
