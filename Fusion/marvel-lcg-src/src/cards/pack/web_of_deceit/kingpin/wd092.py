from . import *

# * Kingpin (II)

def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # « When Revealed: Search the encounter deck and discard pile for the
        # Kingpin's Suit and Kingpin's Cane attachments and attach them to
        # Kingpin. »
        this = effect.this.CastTo(EncounterVillain)
        premier = Worlds.GetFirstPlayer(effect)
        for nom in ("Kingpin's Suit", "Kingpin's Cane"):
            carte = Search.SearchForCard(
                effect,
                premier,
                include_encounter_deck=True,
                include_encounter_discard_pile=True,
                name=nom,
            )
            if carte:
                carte.PutIntoPlay(premier, effect)
                carte.CastTo(Attachment).AttachTo2(this, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
    ]
