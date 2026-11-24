from . import *

# Solar Surge — RESSOURCE, RES [energy], x2.
# Resource: Double the number of resources this card generates if Sunspot has more than 2 solar counters (triple the
#   resources instead if Sunspot has more than 4 solar counters).
#
# CARTES DE REFERENCE
#  - `01055` The Power of Aggression : `AbilityFactory.CheckThisCanDropPay(fn)` ; la fonction rend les ressources que la carte
#    genere (`this.printed_resource`), ici multipliees selon le stock.
#
# TEXTE CONTRE CODE
#  ⚠ « MORE than 2 » : 3 compteurs ou plus -> x2 ; « MORE than 4 » : 5 ou plus -> x3 (jamais x6). Le stock lu est celui du joueur
#    QUI PAIE (`message.GetToPlayer()`), au moment du paiement.


def GetAbilities() -> Sequence['Ability']:

    def solar_surge(effect: 'Effect', message: 'Message.CheckPlayerCanPayCost') -> 'Resources|None':
        this = effect.this.CastTo(Resource)
        res = this.printed_resource
        joueur = message.GetToPlayer()
        stock = SolairesDe(joueur) if joueur is not None else 0
        if stock > 4:
            return res * 3
        if stock > 2:
            return res * 2
        return res

    return [
        AbilityFactory.CheckThisCanDropPay(solar_surge),
    ]
