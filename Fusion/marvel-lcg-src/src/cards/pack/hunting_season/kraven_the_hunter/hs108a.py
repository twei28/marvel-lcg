from . import *

# hs108a The Great Hunt
# When Revealed : cherche The Calypso Serum (paquet et defausse de rencontre), le revele, melange le paquet. Avance a 2B (automatique).

def GetAbilities() -> Sequence['Ability']:

    def serum(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Find.FindAndReveal(
            effect, Worlds.GetFirstPlayer(effect),
            finder=CardFinder(name="The Calypso Serum", card_type=EncounterSideScheme,
                              check_face_fn=lambda f: not f.IsInPlay()),
        )
        Worlds.GetEncounterDeck(effect).Shuffle(effect)

    return [AbilityFactory.WhenThisRevealed(None, serum)]
