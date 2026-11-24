from . import *

# Mind Over Matter (x2 : hf344, hf345). Traitrise PSIONIC SKILL, Boost 1 + [star]. « When Revealed : Reveal the topmost attachment in the encounter discard pile.
# Otherwise, this card gains surge. [star] Boost : Exhaust your hero. »
# Cartes de reference : hf321 (`face.Reveal(joueur, effect)`), 40160 / `ThisCardGainSurge(effect)`, `Worlds.GetEncounterDiscardPileCards` (top en tete : `Deck.Get(True)`).
# ⚠ « topmost » : la PLUS RECENTE defaussee ; « attachment » = type Attachment (les ameliorations et soutiens ne comptent pas) ; « Exhaust your hero » : le HEROS
# (forme heros), pas l'alter-ego ; sous forme alter-ego rien n'est epuise.


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        for face in Worlds.GetEncounterDiscardPileCards(effect):
            if Attachment.IsType(face):
                face.Reveal(joueur, effect)
                return
        ThisCardGainSurge(effect, message)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = message.GetToPlayer()
        identite = joueur.GetIdentity() if joueur is not None else None
        if identite is not None and Hero.IsType(identite):
            Faces.ExhaustAll([identite], effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
