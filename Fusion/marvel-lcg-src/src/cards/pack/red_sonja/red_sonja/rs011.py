from . import *

# Crimson Shadow — amelioration signature, x1 (13/15). PREPARATION. SKILL.
# Cout 2, ressource [B].
# Red Sonja gets +1 THW.
# Uses (2 stealth counters).
# Hero Response: After a minion enters play, remove 1 stealth counter from
# here -> cancel that minion's "When Revealed" effect.
#
# ⚠⚠ ARBITRAGE UTILISATEUR (22/09/2026, question posee AVANT d'ecrire ce
# script) : le texte imprime dit « Hero Response » (APRES coup) pour un
# effet qui ANNULE un « When Revealed » -- techniquement impossible : annuler
# exige d'agir AVANT que l'effet ne se resolve. Reponse retenue : coder en
# INTERRUPT fonctionnel (le seul timing qui puisse reellement produire ce
# que la carte annonce), au prix du mot « Response » imprime. Ecart assume
# et documente ici, pas invente en silence.
#
# CARTES DE REFERENCE
#  - `01078` Get Behind Me! (officiel) : `message.CancelWhenRevealedEffect
#    (effect)`, montage `WhenPlayerRevealCard(Interrupt, "AnyPlayer",
#    Treachery, "WhenRevealed", ..., from_encounter=True)`.
#  - `an009` Xiphos : `AbilityFactory.CanPlayThisUpgradeCard()` (necessaire
#    pour qu'une amelioration simple s'attache a l'identite par defaut) +
#    `GiveKeywordToAttached("You", ...)` pour le bonus de stat passif.
#
# TEXTE CONTRE CODE
#  ⚠ « a minion enters play » (pas « an enemy ») : `which_card=Minion`,
#    `from_encounter=True` (mise en jeu depuis la pioche rencontre).
#  ⚠ « remove 1 stealth counter from here -> cancel » : le retrait du
#    compteur est le COUT (`CostFunc.Counter`), l'annulation est l'effet.

def GetAbilities() -> Sequence['Ability']:

    def crimson_shadow(effect: 'Effect', message: 'Message.WhenPlayerRevealCard') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        message.CancelWhenRevealedEffect(effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            thwart=1,
        ),
        AbilityFactory.WhenPlayerRevealCard(
            AbilityType.HeroInterrupt,
            "AnyPlayer",
            Minion,
            "WhenRevealed",
            crimson_shadow,
            from_encounter=True,
        ).SetCostFunc(CostFunc.Counter("This", 1, 'stealth')),
    ]
