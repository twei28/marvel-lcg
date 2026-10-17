from . import *

# Opportunist — AMELIORATION 2 [physical], Ninjutsu (TMNT Shinobi, Inkwire). SKILL.
# Max 1 per player.
# Hero Action (thwart): Discard a cloaked status card from a character you control and exhaust Opportunist -> remove
# 3 threat from a scheme.
#
# NOUVELLE. Mots-cles (fiches lues AVANT le code) : Cloaked (cloaked.md).
#
# Cartes de reference :
#  - `sk049` The Thing : cout PERSONNALISE « discard a tough status card FROM <personnage> » =
#    `CostFunc.Custom(CardFinder(...), fn)` + `DiscardTough` (ici `CoutDefausserCloaked("controlled")`) ;
#  - `tj006` / `up023` : amelioration sans « Attach to » = `CanPlayThisUpgradeCard()`, `CostFunc.Exhaust("This")` ;
#  - `10019` To the Rescue! : « Remove N threat from a scheme » = `RemoveThreatFromSchemes` + `SetTarget(Scheme2)`.
#
# TEXTE CONTRE CODE
#  ⚠ « from a character YOU CONTROL » : identite ou allie sous votre controle, au choix (pas un personnage d'un autre
#    joueur, pas un ennemi) ; sans Cloaked sur un tel personnage l'action n'est pas proposee.
#  ⚠ « Discard a cloaked status card AND exhaust Opportunist » : DEUX couts, tous deux obligatoires.
#  ⚠ « Max 1 per player » : `MaxPerUnit = 1`. « 3 threat from A scheme » : un seul complot.


def GetAbilities() -> Sequence['Ability']:

    def opportunist(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        this.RemoveThreatFromSchemes(effect.targets, 3, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            opportunist,
        ).SetLabel('thwart')
        .SetCostFunc(CoutDefausserCloaked("controlled"))
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Scheme2),
    ]
