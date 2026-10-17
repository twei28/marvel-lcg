from . import *

# Daitō — AMELIORATION 1 [physical], aspect Aggression (TMNT Aspects, Inkwire). NINJA. WEAPON.
# Attach to a friendly character. While attached to an identity, this card gains restricted.
# Interrupt: When attached character attacks an enemy, exhaust Daitō → this attack deals 1 additional damage
#   and gains piercing.
#
# MOTS-CLES (fiches lues AVANT le code) : restricted.md, piercing.md.
# CARTES DE REFERENCE
#  - `54018` * Bambino : « While attached to an identity, this card gains restricted » =
#    `ThisGainKeyword(lambda: Identity.IsType(bind_face), restricted=1, change_on_event=AttachedMove)` ;
#    « When attached character makes a basic attack ... this attack deals 3 additional damage » =
#    `WhenUnitMakeAttack(Interrupt, "AttachedCharacter", ...)` + `message.DealAdditionalDamage`.
#  - `31029` / `34007` : « Attach to a friendly character » = `CanPlayThisUpgradeCard(Friend)`.
#  - `tc012` Persuader : « This attack gains piercing » = `message.GainPiercing(effect)`.
# TEXTE CONTRE CODE
#  ⚠ « ATTACKS an enemy » (pas « makes a BASIC attack » comme Bambino) : toute attaque, sans `is_basic_attack`.
#  ⚠ « exhaust Daitō → » : cout ; Daito incline ne peut plus servir avant d'etre redresse.
#  ⚠ « 1 additional damage AND gains piercing » : les deux.


def GetAbilities() -> Sequence['Ability']:

    def daito(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        message.DealAdditionalDamage(1, effect)
        message.GainPiercing(effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(Friend),
        AbilityFactory.ThisGainKeyword(
            lambda effect, ui: Identity.IsType(effect.this.CastTo(Upgrade).bind_face),
            restricted=1,
            change_on_event=OnEvent.AttachedMove("This"),
        ),
        AbilityFactory.WhenUnitMakeAttack(
            AbilityType.Interrupt,
            "AttachedCharacter",
            daito,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
