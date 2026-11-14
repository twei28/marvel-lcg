from . import *

# "Where's My Rent!?" (7) — PISTE. Response : While in Soho, after you play an event, place 1 rent counter here. Then, if there are 3 or more
#   counters here, add this card to the victory display, reveal the top LEAD card, and draw 1 card.
#
# Cartes de reference : `AbilityFactory.AfterPlayerPlayedCard` (game/ability/factory/play.py), fiche piste-lead.md.

def GetAbilities() -> Sequence['Ability']:

    def apres(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        CompteurPuisFin(effect, Joueur(effect), 'rent', 3)

    return [AbilityFactory.AfterPlayerPlayedCard(AbilityType.Response, "You", Event, apres, conditions=[EnLieu("pu036")])]
