from . import *

# The City — ENVIRONNEMENT. Setup. Permanent.
# • Players mark their location in the city with a token, starting in Midtown.
# • Players can only interact with locations (abilities & cards attached) they occupy.
# Action: Exhaust a character you control or spend 1 resource of any type → move to an adjacent (↔ or ↕) location.
#
# Cartes de reference : mu004 (Graffitied Streets : environnement a Action payee par `CostFunc.Exhaust("YouControlUnit")`),
# pu121 (`CostFunc.Spend(Cost("1"))`, « 1 ressource de n'importe quel type »), gmw/16073b (`SetTarget(lambda effect: ...)` :
# la cible est choisie dans une liste calculee), brique `Ville` (spec M1/M2).
# ⚠ Les deux premieres puces sont des regles de MISE EN PLACE et d'acces : la position de depart est posee par `Ville.Installer`
# (scenario) et l'acces aux lieux par `Ville.AuLieu` sur chaque carte de lieu ; elles n'ont pas de capacite propre.
# ⚠ « Exhaust a character you control OR spend 1 resource » : deux Actions jumelles (meme effet, un cout chacune) : le joueur
# choisit son cout en choisissant l'Action. Pas de limite par round (FAQ du livret).

def GetAbilities() -> Sequence['Ability']:

    def voisins(effect: 'Effect') -> Sequence['CardFace']:
        etat = Ville.Etat(effect)
        joueur = effect.GetInitiator()
        case = None if etat is None else Ville.Case(effect, joueur)
        if etat is None or case is None:
            return []
        return [etat.cases[v] for v in Ville.Adjacentes(effect, case)]

    def se_deplacer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        cibles = effect.targets
        if not cibles:
            return
        case = Ville.CaseDe(effect, cibles[0])
        if case is not None:
            Ville.Deplacer(effect, effect.GetInitiator(), case)

    def ville_en_place(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        Unused(message)
        return Ville.Etat(effect) is not None

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, se_deplacer, conditions=[ville_en_place])
        .SetCostFunc(CostFunc.Exhaust("YouControlUnit"))
        .SetTarget(voisins, is_optional=False),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, se_deplacer, conditions=[ville_en_place])
        .SetCostFunc(CostFunc.Spend(Cost("1")))
        .SetTarget(voisins, is_optional=False),
    ]
