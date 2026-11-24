from . import *

def GetAbilities() -> Sequence['Ability']:
    def reveler(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        if joueur is None:
            return
        faces = joueur.DiscardDeckTopCards(1, effect)
        if not faces:
            return
        couleurs = Types(faces[0])
        if not couleurs:
            return
        cibles = [f for f in joueur.hand_cards.Get() if Types(f) & couleurs]
        if cibles:
            Faces.DiscardAll(cibles, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, reveler),
    ]
