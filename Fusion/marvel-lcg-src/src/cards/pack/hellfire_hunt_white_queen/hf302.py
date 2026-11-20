from . import *

# White Queen (sbire PSIONIC, module Perfection). Elite, Guard, Patrol (desc). « When Revealed : Reveal the topmost ILLUSION attachment in the
# encounter discard pile. Forced Interrupt : When a White Queen minion attempts to enter play, give the engaged player a facedown encounter card
# and discard this card. » Cartes de reference : 32151 Master of Magnetism (`GetEncounterDiscardPile(...).FindTopmost(CardFinder2(trait))`).


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        face = Worlds.GetEncounterDiscardPile(effect).FindTopmost(CardFinder2(ILLUSION, Attachment))
        if face is not None and joueur is not None:
            face.Reveal(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
        SbireWQEntreEnJeu(),
    ]
