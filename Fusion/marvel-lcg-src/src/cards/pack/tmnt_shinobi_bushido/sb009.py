from . import *

# Devotion — AMELIORATION OATH, classe Bushido (Inkwire, TMNT Shinobi). Cout 1, [energy].
# Uses (3 samurai counters).
# Hero Action: Exhaust this card and remove 1 samurai counter from it -> ready a WEAPON upgrade you control.
# « Mastery does not come quickly. » —Ronin
#
# Mots-cles (fiches lues AVANT le code) : Uses (uses.md, NATIF) ; samurai counter / OATH (samurai-counter.md).
#
# Cartes de reference :
#  - « Hero Action: Exhaust this card and remove 1 samurai counter from it -> » : `jennika/tj006` Fearless Resolve
#    (`CostFunc.Exhaust("This")` + `CostFunc.Counter("This", n, 'samurai')`) ;
#  - « ready <cible> » avec cible filtree `canbe_ready=True` : `nebu/22014` Justice Served (`SetTarget("YourHero", canbe_ready=True)`)
#    + `Faces.ReadyAll(effect.targets, effect)` ;
#  - « <amelioration> you control » (identite ET allies) : `joueur.GetControlUpgrade(CardFinder(trait=...))` (modele `se003`).
#
# TEXTE CONTRE CODE
#  ⚠ « Hero Action » : forme heros seule.
#  ⚠ « Exhaust this card AND remove 1 samurai counter FROM IT » : deux couts ; Uses defausse la carte au dernier compteur.
#  ⚠ « ready A WEAPON upgrade YOU control » : UNE amelioration de trait WEAPON sous son controle (celle d'un allie comprise),
#    inclinee (une amelioration deja prete n'est pas une cible legale, comme pour `canbe_ready` de Justice Served) ; Devotion
#    elle-meme n'est pas une arme.


def GetAbilities() -> Sequence['Ability']:

    def armes_sous_controle(effect: 'Effect') -> 'Sequence[CardFace]':
        joueur = effect.GetInitiator()
        if joueur is None:
            return []
        return list(joueur.GetControlUpgrade(CardFinder(trait="WEAPON")))  # type: ignore

    def devotion(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        Faces.ReadyAll(effect.targets, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            devotion,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'samurai'))
        .SetTarget(armes_sous_controle, canbe_ready=True),
    ]
