from . import *

# Play the Market (8) — PISTE. Response : While in the Financial District, after you defend an attack, place 1 stock counter here. Then, if
#   there are 3 or more counters here, add this card to the victory display, reveal the top LEAD card, and draw 1 card.
#
# Cartes de reference : `AbilityFactory.AfterUnitDefendAgainstAttack` (game/ability/factory/do_attack.py), fiche piste-lead.md.
# ⚠ « you defend » : le joueur declare un defenseur (identite ou allie) contre une attaque ; une attaque non defendue ne compte pas.

def GetAbilities() -> Sequence['Ability']:

    def apres(effect: 'Effect', message: 'Message.AfterUnitDefendEnd') -> None:
        CompteurPuisFin(effect, Joueur(effect), 'stock', 3)

    return [AbilityFactory.AfterUnitDefendAgainstAttack(AbilityType.Response, "You", apres, conditions=[EnLieu("pu037")])]
