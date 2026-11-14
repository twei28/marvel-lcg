from . import *

# Village of the Damned (4) — PISTE. Response : While in West Village, after you reveal an encounter card, place 1 curse counter here.
#   Then, if there are 4 or more counters here, add this card to the victory display, reveal the top LEAD card, and draw 1 card.
#
# Cartes de reference : `AbilityFactory.AfterPlayerRevealCard` (game/ability/factory/reveal.py), fiche piste-lead.md.
# ⚠ « you reveal » : une carte de rencontre revelee POUR ce joueur (dont celle de West Village qui en donne une de plus) ; seuil 4 (pas 3).

def GetAbilities() -> Sequence['Ability']:

    def apres(effect: 'Effect', message: 'Message.AfterCardRevealedEnd') -> None:
        CompteurPuisFin(effect, Joueur(effect), 'curse', 4)

    return [AbilityFactory.AfterPlayerRevealCard(AbilityType.Response, "You", CardFace, apres, conditions=[EnLieu("pu033")])]
