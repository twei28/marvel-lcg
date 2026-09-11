from . import *

# * Mount Olympus (soutien, cout 1, LOCATION OLYMPUS, physique)
# Resource: Exhaust Mount Olympus and spend a [energy] resource → generate a
# [lightning] resource.
#
# La seconde source d'ECLAIR du pack, avec les quatre Thunder Strike.
#
# ⚠ PAS `CostFunc.Spend(Cost("Y"))` (essaye le 11/09/2026, modele Cloak
# 60020). Spend ouvre un PAIEMENT DANS LE PAIEMENT (`AskSpendResourcesInternal`)
# qui REMET LE POOL A ZERO : les energies deja generees pour la carte en cours
# disparaissaient (« total YY » puis « total L » au journal), et la carte payee
# echouait. Un cout de ressource pendant un paiement doit PRELEVER dans le pool
# courant, pas ouvrir une nouvelle question.
#
# D'ou `CostFunc.Custom` : au moment ou Mount Olympus genere (les couts sont
# payes juste avant `res_pool.Gain`, resources.py:404), on retire UNE energie
# du pool (un joker a defaut, il vaut n'importe quelle couleur). S'il n'y en a
# pas, le cout n'est pas payable et le moteur annule ce moyen de paiement
# (`GameSignal_UndoRequest`) : le joueur doit d'abord depenser une energie,
# puis Mount Olympus. Modele du cout arbitraire : ho009 (RECETTES §5).

def GetAbilities() -> Sequence['Ability']:

    def prelever_une_energie(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(targets)
        joueur = effect.GetInitiator()
        pool = joueur.res_pool.Get()
        if pool.GetColor("Y", convert_green_res=False) >= 1:
            joueur.res_pool.Gain(Resources("Y") * -1, effect)
            return True
        if pool.GetColor("G", convert_green_res=False) >= 1:
            joueur.res_pool.Gain(Resources("G") * -1, effect)
            return True
        return False

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("L"),
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Custom(None, prelever_une_energie)),
    ]
