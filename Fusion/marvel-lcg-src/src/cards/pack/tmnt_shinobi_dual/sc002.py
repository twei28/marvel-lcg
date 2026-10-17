from . import *

# Shugorei — AMELIORATION DUALE Bushido/Kuji-Kiri, cout 2, [mental]. OATH. SPELL.
# Classe : « Bushido;Kuji-Kiri ».
# Max 1 per player. Uses (4 samurai counters).
# Action: Exhaust this card and remove 2 samurai counters from it -> draw 1 card.
#
# Mots-cles (fiches lues AVANT le code) : Uses (uses.md) ; samurai counter / OATH (samurai-counter.md) ; Max N per player
# (base native `desc.MaxPerUnit`).
#
# Cartes de reference :
#  - deux couts chaines « Exhaust this card AND remove N counters from it » : `jennika/tj006` Fearless Resolve
#    (`CostFunc.Exhaust("This")` + `CostFunc.Counter("This", n, 'samurai')`, `CanPlayThisUpgradeCard`) ;
#  - « Max 1 per player » : `01018` Energy Channel (`desc.MaxPerUnit = "1"`, aucun script) ;
#  - `DrawUp(n, effect)` : `mf011`.
#
# TEXTE CONTRE CODE
#  ⚠ « Uses (4 samurai counters) » : base native `desc.Uses = "4,samurai"` ; 4 compteurs a l'entree en jeu.
#  ⚠ « Exhaust this card AND remove 2 samurai counters FROM IT » : DEUX couts obligatoires, les compteurs sont pris SUR
#    CETTE carte (pas sur une autre amelioration OATH). Deux utilisations au plus (4 compteurs, 2 par usage) ; au 2e usage la
#    carte perd son dernier compteur et quitte le jeu (Uses).
#  ⚠ « Action » (et non « Hero Action ») : utilisable en forme heros ET alter-ego. « draw 1 card » : le joueur qui l'utilise.
#  ⚠ « Max 1 per player » : un seul exemplaire en jeu par joueur (MaxPerUnit).


def GetAbilities() -> Sequence['Ability']:

    def shugorei(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        joueur.DrawUp(1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            shugorei,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 2, 'samurai')),
    ]
