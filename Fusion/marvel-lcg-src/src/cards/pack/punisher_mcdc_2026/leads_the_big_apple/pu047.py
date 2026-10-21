from . import *

# Forget It... It's Chinatown (9) — PISTE. Response : While in Chinatown, after you defeat a minion, place 1 takeout counter here. Then if there
#   are 2 or more counters here, add this card to the victory display, reveal the top LEAD card, and draw 1 card.
#
# Cartes de reference : `AbilityFactory.AfterUnitDefeatedUnit` (game/ability/factory/defeated.py), fiche piste-lead.md. Seuil 2 (pas 3).

def GetAbilities() -> Sequence['Ability']:

    def apres(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        CompteurPuisFin(effect, Joueur(effect), 'takeout', 2)

    return [AbilityFactory.AfterUnitDefeatedUnit(AbilityType.Response, "You", Minion, apres, conditions=[EnLieu("pu038")])]
