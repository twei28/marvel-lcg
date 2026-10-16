from . import *

# Hittin' the Town : « Discard cards from the top of the villain deck until an
# attachment or side scheme is discarded and reveal it. »
# TODO-QUESTION Q5 : « villain deck » lu comme le DECK RENCONTRE (le scenario n'a pas
# de deck de vilain a defausser, et Anchovy dit « encounter deck »).

def GetAbilities() -> Sequence['Ability']:

    def type_voulu(face: 'CardFace') -> bool:
        return Attachment.IsType(face) or EncounterSideScheme.IsType(face)

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        # Rien a trouver nulle part : on ne boucle pas (deck + defausse).
        faces = list(Worlds.GetEncounterDeckCards(effect)) + list(Worlds.GetEncounterDiscardPileCards(effect))
        if not any(type_voulu(f) and not f.IsInPlay() for f in faces):
            return
        face = Worlds.DiscardEncounterCardsUntil(effect, check_face_fn=type_voulu)
        if face is not None:
            face.Reveal(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
    ]
