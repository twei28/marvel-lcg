from . import *

# * Mystique (Raven Darkholme) : ALLIE (X-MEN), cout 3, PV 3, THW 2*, ATQ 2*, ressource [wild].
# Action: Exhaust Mystique and spend a resource of any type -> heal 1 damage from your identity and ready your identity. (Limit once per phase.)
#
# CARTES DE REFERENCE
#  - `48001a` Nightcrawler : `WhenInYourPlayTurn(Action, op).SetCost(Cost("1")).LimitOncePerPhase()` (« spend 1 resource of any type »).
#  - `17007` Element Gun : `.SetCostFunc(CostFunc.Exhaust("This"))` en plus du cout de ressource.
#  - `01080` First Aid / mt `SoignerUnAmi` : `HealthUnits([cible], n, effect)` ; `Faces.ReadyAll`.
#
# TEXTE CONTRE CODE
#  « ready YOUR IDENTITY » (FR 1.2 : « redressez votre identite », l'EN beta disait « ready it ») : l'identite du joueur, pas Mystique (qui vient d'etre inclinee). « heal 1 damage FROM YOUR IDENTITY » : l'identite,
#    pas un autre personnage. « a resource OF ANY TYPE » : `Cost("1")`. « Limit once per phase » : `LimitOncePerPhase`.
#  Chiffres : cout 3, PV 3, THW 2*, ATQ 2*, 1 ressource, 1 soin.


def GetAbilities() -> Sequence['Ability']:

    def mystique(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)
        joueur = effect.GetInitiator()
        identite = joueur.GetIdentity()
        this.HealthUnits([identite], 1, effect)
        Faces.ReadyAll([identite], effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            mystique,
        ).SetCost(Cost("1"))
        .SetCostFunc(CostFunc.Exhaust("This"))
        .LimitOncePerPhase(),
    ]
