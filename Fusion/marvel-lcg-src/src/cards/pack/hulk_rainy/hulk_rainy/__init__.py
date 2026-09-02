from cards.pack import *

def SurpaiementEnergieOuPhysique(effect: 'Effect', cout_imprime: int) -> bool:
    """hk005 Interception : « If you OVERPAID for this card with a [energy] or
    [physical] resource ».

    Transposition de `EnergyOverpaid` (pack wonder_man, 58005 Starstruck), a
    deux differences pres : deux couleurs sont acceptees au lieu d'une, et on
    ne rend qu'un booleen, la carte n'ayant pas d'effet proportionnel.

    « Overpaid » ne veut pas dire « a paye avec » : il faut que le paiement
    DEPASSE le cout imprime, ET que la couleur en question ait ete depensee.
    Interception coute 0 : tout paiement est donc un surpaiement, mais il doit
    quand meme contenir une ressource energie ou physique — un mental seul ne
    declenche rien.

    `convert_green_res=False` : un wild ne compte pas comme energie ni comme
    physique. Meme lecture que 58005 et que le Recharge de vv001b.
    """
    paye = effect.GetPaidResources()
    surplus = paye.val - cout_imprime
    if surplus <= 0:
        return False
    energie = paye.GetColor('Y', convert_green_res=False)
    physique = paye.GetColor('R', convert_green_res=False)
    return (energie + physique) > 0
