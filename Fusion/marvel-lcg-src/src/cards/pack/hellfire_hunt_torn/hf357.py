from . import *

# Narrow Minded (obligation ILLUSION PSIONIC, Boost 2, icone Amplify ; x2 : hf357, hf358). « Alter-Ego Action : Exhaust your identity -> discard this card. »
# L'icone au centre (avion + croix) est AMPLIFY (livret p.4, comparee a 16054 Vendetta) : `desc.Amplify = 1`, natif (+ `HasAmplify` ajoute a `Obligation`, voir le journal
# de portage). Cartes de reference : 11049 Fear of Kang / 40160 (`PlayerActionToDiscardThis(AlterEgoAction).SetCostFunc(CostFunc.Exhaust("YourIdentity"))`).


def GetAbilities() -> Sequence['Ability']:
    return [AbilityFactory.PlayerActionToDiscardThis(AbilityType.AlterEgoAction).SetCostFunc(CostFunc.Exhaust("YourIdentity"))]
