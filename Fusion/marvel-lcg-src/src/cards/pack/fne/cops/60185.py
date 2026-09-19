from . import *

# Police Cordon (side scheme) — Hinder 1[per_hero] : base automatique.
# Each POLICE minion gains guard and patrol.
# When Revealed: Search the encounter deck and discard pile for a POLICE minion
#   and reveal it.
#
# Modeles : GiveKeywordToInPlayWhenApplyThis (rend une LISTE, deballage *),
# 01095 Rhino pour la recherche + Reveal.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        face = Search.EncounterCard(
            effect,
            include_discard_pile=True,
            trait="POLICE",
            card_type=Minion,
        )
        if face:
            face.Reveal(joueur, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(trait="POLICE", card_type=Minion),
            guard=1,
            patrol=1,
        ),
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
