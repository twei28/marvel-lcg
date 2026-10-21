from . import *

# A Walk in the Park (3) — PISTE. Response : While in Upper East Side, after you defeat a side scheme, add this card to the victory display,
#   reveal the top LEAD card, and draw 1 card.
#
# Cartes de reference : `AbilityFactory.AfterUnitDefeatedScheme(..., "You", ...)` (game/ability/factory/scheme.py), fiche piste-lead.md.
# ⚠ Pas de compteur : une seule manigance annexe vaincue suffit.

def GetAbilities() -> Sequence['Ability']:

    def apres(effect: 'Effect', message: 'Message.AfterUnitDefeatedScheme') -> None:
        PisteTerminee(effect, Joueur(effect))

    return [AbilityFactory.AfterUnitDefeatedScheme(AbilityType.Response, "You", SchemeSide2, apres, conditions=[EnLieu("pu032")])]
