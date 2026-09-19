from . import *

# * Black Cat (THIEF UNDERLING) — SCH 1 / ATK 1 / 6 PV, boost 2. Villainous : base.
# While there is 4 threat here, treat Black Cat as an ally that takes 2
#   consequential damage after she attacks or thwarts.
# Hero Action: Spend a [mental] resource -> place 1 threat here. If there is 4
#   threat here, take control of Black Cat as an ally.
# La menace sur un sbire est un JETON 'threat' (60145 Baron Zemo, jetons sur
# un allie ; harnais : cle `jetons`). La seule source de menace « here » est
# l'action : la conversion se fait a ce moment (ConvertirBlackCatEnAlliee).
# Alliee, elle garde Villainous (FAQ du livret) : le gabarit fne_black_cat_ally
# le porte, et un allie villainous recoit une carte boost a chaque attaque.

def GetAbilities() -> Sequence['Ability']:

    def placer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Minion)
        joueur = effect.GetInitiator()
        Faces.PlaceTokensOn([this], 1, 'threat', effect)
        if this.GetTokens('threat') >= 4:
            ConvertirBlackCatEnAlliee(this, joueur, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, placer)
            .SetName("Spend a mental resource: place 1 threat on Black Cat")
            .SetCost(Cost("B")),
    ]
