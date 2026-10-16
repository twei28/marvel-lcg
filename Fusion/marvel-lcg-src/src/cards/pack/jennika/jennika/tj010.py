from . import *

# * Jennika's Other Tekko-Kagi — AMELIORATION signature, x1 (15/15, jumelle de tj009).
# NINJA. TEKKO-KAGI. WEAPON. Cout 1, [energy].
# Each [[TEKKO-KAGI]] upgrade you control gains: "Hero Interrupt: When you make a basic
#   attack, exhaust this card and discard 1 card from your hand -> Jennika gets +2 ATK
#   for that attack. This attack gains piercing."
#
# Cartes de reference :
#  - octroi : `michelangelo/tm012` (meme montage « each X upgrade you control gains ») ;
#  - « When you make a basic attack ... +N ATK ... gains piercing » : `cw/56017` Savage
#    Strike (`WhenUnitMakeAttack(HeroInterrupt, "You", op, is_basic_attack=True)` +
#    `message.GainATKForThisAttack` + `message.GainPiercing`) ; cout incliner :
#    `mf008` Neutralizer ; cout defausser 1 carte : `tm001b`.
#
# ⚠ Mots-pieges :
#  - « EACH TEKKO-KAGI upgrade you control gains » : meme lecture que tj009 (tj010
#    elle-meme comprise) ; chaque exemplaire s'incline a part ;
#  - « When you make a BASIC attack » : attaque de base seulement, pas un evenement
#    d'attaque ;
#  - « exhaust this card AND discard 1 card from your hand -> » : DEUX couts AVANT la
#    fleche, tous deux obligatoires ;
#  - « Jennika gets +2 ATK FOR THAT ATTACK » : +2 pour cette attaque seulement,
#    pas jusqu'a la fin du round ; « This attack gains piercing » : inconditionnel ;
#  - « Hero Interrupt » : forme heros uniquement.


def GetAbilities() -> Sequence['Ability']:

    def attaque_tekko_kagi(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.GainATKForThisAttack(2, effect)
        message.GainPiercing(effect)

    interruption_donnee = AbilityFactory.WhenUnitMakeAttack(
        AbilityType.HeroInterrupt,
        "You",
        attaque_tekko_kagi,
        is_basic_attack=True,
    ).SetCostFunc(CostFunc.Exhaust("This")) \
     .SetCostFunc(CostFunc.Discard("YourHandCards", range=(1, 1)))

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(trait="TEKKO-KAGI", card_type=Upgrade),
            control_by="You",
            given_abilities=[interruption_donnee],
        ),
    ]
