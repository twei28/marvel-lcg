from . import *

# hs119 / hs120 The Hunt Begins
# When Revealed : defausse 3 x (etape du vilain) cartes du paquet de rencontre ; revele le premier attachement ITEM ou WEAPON defausse ainsi, sinon distribue un piege.

def GetAbilities() -> Sequence['Ability']:

    def chasse(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        vilain = Vilain(effect)
        etape = vilain.printed_stage if vilain is not None else 1
        defaussees = Worlds.DiscardEncounterCards(3 * etape, effect)
        for face in defaussees:
            if Attachment.IsType(face) and (face.HasTrait("ITEM") or face.HasTrait("WEAPON")):
                face.Reveal(joueur, effect)
                return
        DonnerPiege(effect, joueur)

    return [AbilityFactory.WhenThisRevealed(None, chasse)]
