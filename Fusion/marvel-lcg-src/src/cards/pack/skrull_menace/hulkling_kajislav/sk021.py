from . import *

# Deflect the Blow — amelioration d'aspect PROTECTION (n° 21). PREPARATION.
# Cout 1 [physical].
# Hero Interrupt (defense): When you would take any amount of damage from an
#   attack, discard Deflect the Blow and exhaust your hero, prevent all of that
#   damage.
#
# Cartes de reference :
#  - **`50042`** * EM Shield : « Interrupt (defense): When you would take any
#    amount of damage from an attack, discard EM Shield → prevent all of that
#    damage. » MEME phrase : `WhenUnitWouldTakeDamage(..., "You", op,
#    is_from_attack=True).SetLabel('defense').SetCostFunc(Discard("This"))` +
#    `message.PreventDamage("All", effect)`.
#  - `CostFunc.Exhaust("YourHero")` (33 cartes) pour « and exhaust your hero ».
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **Hero** Interrupt » : forme heros (EM Shield n'a qu'un Interrupt nu).
#  - « discard ... **and** exhaust your hero » : les DEUX font le cout. Un heros
#    deja incline ne peut pas payer : la capacite n'est pas offerte. Or
#    DEFENDRE incline le heros avant les degats : la carte sert donc contre une
#    attaque NON defendue encadree par un heros encore pret (ou redresse).
#  - Ecrit sans fleche, mais « discard X and exhaust Y, prevent » = cout puis
#    effet, comme EM Shield.
#  - « When **you** would take » : l'identite, pas un allie.
#  - « all of that damage » : `PreventDamage("All")`.
#  - « (defense) » : `SetLabel('defense')`.


def GetAbilities() -> Sequence['Ability']:

    def devier(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        message.PreventDamage("All", effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            devier,
            is_from_attack=True,
        ).SetLabel('defense')
        .SetCostFunc(CostFunc.Discard("This"))
        .SetCostFunc(CostFunc.Exhaust("YourHero")),
    ]
