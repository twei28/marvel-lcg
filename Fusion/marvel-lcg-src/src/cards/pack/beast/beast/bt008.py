from . import *

# Primal Rage — evenement signature, x2. X-MEN. Cout 0.
# Hero Interrupt: When you make a basic attack, discard a card from your
# hand -> you get +5 ATK for that attack.
#
# Carte de reference :
#  - 19005 Knife Leap (Drax) : « Hero Interrupt: When you make a basic attack,
#    you get +5 ATK for that attack. » Meme declencheur, meme valeur, meme
#    fabrique `WhenUnitMakeAttack(AbilityType.HeroInterrupt, "You", op,
#    is_basic_attack=True).SetPlay().SetLabel()` et meme
#    `message.GainATKForThisAttack(5, effect)`. Knife Leap ajoute overkill et
#    piercing la ou Primal Rage demande une defausse : c'est la seule
#    difference, et elle est du cote du COUT.
#  - le cout de defausse : 45014 Advanced Suit,
#    `.SetCostFunc(CostFunc.Discard("YourHandCards"))`.
#
# ⚠ « discard a card from your hand » est ecrit AVANT la fleche `→` : c'est le
# COUT, pas l'effet (meme lecture que an006, cf. son commentaire). Le coder en
# effet laisserait jouer la carte sans main, et donnerait les +5 ATK gratis.
#
# ⚠ `is_basic_attack=True` : le texte dit « basic attack », donc l'attaque de
# l'identite avec son ATK, pas une attaque d'evenement (meme distinction que
# 01024 One-Two Punch, « using your ATK »).

def GetAbilities() -> Sequence['Ability']:

    def primal_rage(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        message.GainATKForThisAttack(5, effect)

    return [
        AbilityFactory.WhenUnitMakeAttack(
            AbilityType.HeroInterrupt,
            "You",
            primal_rage,
            is_basic_attack=True,
        ).SetPlay().SetLabel()
        .SetCostFunc(CostFunc.Discard("YourHandCards")),
    ]
