from . import *

# From The Ashes : ressource Basic. Max 2 per deck.
# This card doubles the number of resources it generates while paying for the first card you play in your turn.
#
# Cartes de reference : 01055 The Power of Aggression (`AbilityFactory.DoubleResourcesThisGenerates`, resources.py:66, modele de ce
# script), `AbilityFactoryResources.CheckThisCanDropPay(fn)` (resources.py:93).
# ⚠ « the FIRST card you play in your TURN » : `this_turn_played_cards` vide ; sans ce filtre (carte suivante du tour) la ressource vaut 1.
def GetAbilities() -> Sequence['Ability']:
    def cendres(effect: 'Effect', message: 'Message.CheckPlayerCanPayCost') -> 'Resources|None':
        this = effect.this.CastTo(Resource)
        res = this.printed_resource
        joueur = JoueurDe(effect)
        paye = message.paying_for_card
        if paye is not None and joueur is not None and HasCost.IsType(paye) and res.val <= message.cost.val \
                and len(joueur.stat.this_turn_played_cards) == 0:
            res *= 2
        return res

    return [
        AbilityFactory.CheckThisCanDropPay(cendres),
    ]
