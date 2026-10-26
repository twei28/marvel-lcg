from . import *

# * Radiant Avenger — AMELIORATION (TITLE), cout 2, RES [physical]. Unique.
# Sunspot gains the AVENGER trait.
# Hero Action: Exhaust this card and remove 1 solar counter from Sunspot -> Sunspot gains +1 ATK until the end of the round.
# Action: Exhaust this card -> place 1 solar counter on Sunspot.
#
# CARTES DE REFERENCE
#  - `01017` Cosmic Flight : `*AbilityFactory.GiveKeywordToAttached(CardFinder(name=..), trait="AERIAL")` pour « gains the X trait ».
#  - `14022` Adrenaline Rush : `hero.GainUntilPhaseEnd(effect, attack=1)` ; ici `GainUntilRoundEnd` (meme famille, fin du ROUND).
#  - `sw001b` : poser un compteur sur l'identite.
#
# TEXTE CONTRE CODE
#  ⚠ « Exhaust this card AND remove 1 solar counter -> » : deux couts, la carte et le compteur.
#  ⚠ L'Action (sans « Hero ») sert dans les deux formes ; la Hero Action seulement en forme heros.


def GetAbilities() -> Sequence['Ability']:

    def radiant_avenger_attack(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        Unused(message)
        effect.GetInitiator().GetHero().GainUntilRoundEnd(effect, attack=1)

    def radiant_avenger_recharge(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        Unused(message)
        PoserSolaires(effect.GetInitiator(), 1, effect)

    return [
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name="Sunspot"),
            trait="AVENGER",
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            radiant_avenger_attack,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("YourIdentity", 1, COMPTEUR)),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            radiant_avenger_recharge,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
