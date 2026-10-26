from . import *
# Utility Belt — AMELIORATION cout 2 [wild]. ITEM. TECH. Hero Response : after resolving the « When Revealed » effect or boost ability of a deterrence
# card, exhaust Utility Belt -> resolve that card's « When Revealed » effect 1 additional time and cancel its surge effect.
# Reference : sm/27083 (`Faces.ResolveAbility(..., AbilityType.WhenRevealed, ...)`) ; surge : `CanSurge.GainSurge(-n)`.
def GetAbilities() -> Sequence['Ability']:
    def belt(effect: 'Effect', message: 'Message.AfterEffectResolved') -> None:
        carte = message.trigger
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None or carte is None:
            return
        EtatBm(carte)["sans_surge"] = True
        Faces.ResolveAbility([carte], joueur, AbilityType.WhenRevealed, effect)
        if carte.surge:
            carte.GainSurge(-carte.surge, effect)
    return [
        AbilityFactory.AfterCardResolveAbility(
            AbilityType.HeroResponse, None, CardFinder(trait=TRAIT_DISSUASION), belt,
            conditions=[EstUneResolutionDeDissuasion],
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
