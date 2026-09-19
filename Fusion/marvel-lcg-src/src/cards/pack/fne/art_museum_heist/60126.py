from . import *

# Art Thief (THIEF)
# When Revealed: Search the encounter deck and discard pile for an ART
#   attachment and attach it to the villain. If you cannot, move an ART
#   attachment from an identity to the villain.
# [star] Boost: Move an ART attachment from an identity to the villain.
#
# Modeles : 01095 Rhino (Search.EncounterCard include_discard_pile), l'attache
# passe par PutIntoPlay : l'oeuvre s'accroche elle-meme au vilain
# (AttachToFaceWhenPutIntoPlay), sans declencher son Surge (pas de Reveal).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        face = Search.EncounterCard(
            effect,
            include_discard_pile=True,
            trait="ART",
            card_type=Attachment,
        )
        if face:
            face.PutIntoPlay(joueur, effect)
        else:
            DeplacerUneOeuvreVersLeVilain(effect, joueur)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        DeplacerUneOeuvreVersLeVilain(effect, message.GetToPlayer())

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
