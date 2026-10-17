from . import *

# Yoshimitsu — PATH hybride (avance), classes Bushido + Kuji-Kiri (Inkwire, TMNT Shinobi). BUSHIDO. KUJI-KIRI.
# Permanent. You get -1 hand size. You get +2 hit points.
# Magnificence — Hero Action: Take 1 damage and exhaust this card -> you get +1 THW, +1 ATK, and +1 DEF
#   until the end of the round.
#
# Mots-cles (fiches lues AVANT le code) : Permanent (permanent.md) ; Shinobi / Path (shinobi.md).
#
# Cartes de reference :
#  - « -1 hand size » : `sentinel/st005b` ; « +N hit points » : `04160b` Improved Attack Upgrade
#    (`GiveKeywordToAttached("You", health=1)` -> ici `GiveKeywordToInPlayWhenApplyThis("You", health=2)`) ;
#  - « take 1 damage AND exhaust this card -> » : `45043` Blood Rage (`CostFunc.TakeDamage(1, "YourIdentity")` +
#    `CostFunc.Exhaust("This")`) ;
#  - « +1 THW, +1 ATK, +1 DEF until the end of the round » : `jennika/tj001a` Ninja Senpai
#    (`GainUntilRoundEnd(effect, thwart=1, attack=1, defense=1)`).
#
# TEXTE CONTRE CODE
#  ⚠ « You get +2 hit points » : le heros ET l'alter-ego ("You") portent +2 PV max.
#  ⚠ « Take 1 damage AND exhaust this card » : deux couts ; le degat est subi par l'identite (« take »), et le
#    cout n'est paye que si le degat n'est pas prevenu.
#  ⚠ « YOU get +1 THW, +1 ATK, +1 DEF until the end of THE ROUND » : le heros, trois bonus, jusqu'a la fin du
#    round (Hero Action : forme heros).


def GetAbilities() -> Sequence['Ability']:

    def magnificence(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Path)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None or not joueur.IsHero():
            return
        joueur.GetHero().GainUntilRoundEnd(effect, thwart=1, attack=1, defense=1)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis("You", hand_size=-1, health=2),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            magnificence,
        ).SetCostFunc(CostFunc.TakeDamage(1, "YourIdentity"))
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
