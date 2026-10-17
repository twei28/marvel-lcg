from . import *

# Senkon — AMELIORATION 1 [physical], aspect Protection (TMNT Aspects, Inkwire). NINJA. WEAPON.
# Attach to a friendly character. While attached to an identity, this card gains restricted.
# Interrupt: When attached character defends against an enemy attack, exhaust Senkon -> that enemy gets
#   –1 ATK for that attack.
#
# NOUVELLE. MOT-CLE (fiche lue AVANT le code) : Restricted (restricted.md) — limite portee par le moteur ;
# ici le mot-cle est GAGNE sous condition, comme `54018` Bambino.
#
# CARTES DE REFERENCE
#  - `54018` Bambino : « Attach to a ... character. While attached to an identity, this card gains
#    restricted » = `ThisGainKeyword(lambda ...: Identity.IsType(bind_face), restricted=1,
#    change_on_event=OnEvent.AttachedMove("This"))` (copie exacte).
#  - `38014` Judoka Skill : « when you defend against an enemy attack ... the enemy gets -2 ATK for this
#    attack » = `WhenUnitDefendAgainstAttack(Interrupt, ..., against_who=Enemy)` +
#    `message.would_atk_message.GainATKForThisAttack(-2, effect)`.
#  - `CanPlayThisUpgradeCard(Friend)` : « a friendly character » (identite ou allie, de tout joueur).
#
# TEXTE CONTRE CODE
#  ⚠ « ATTACHED character defends » : le porteur (`"AttachedCharacter"`), qu'il soit identite ou allie.
#  ⚠ « against an ENEMY attack » : `against_who=Enemy`.
#  ⚠ « exhaust Senkon -> » : cout ; « that enemy gets –1 ATK for THAT attack » : l'attaque en cours.


def GetAbilities() -> Sequence['Ability']:

    def senkon(effect: 'Effect', message: 'Message.WhenUnitWouldDefend') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        message.would_atk_message.GainATKForThisAttack(-1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(Friend),
        AbilityFactory.ThisGainKeyword(
            lambda effect, ui: Identity.IsType(effect.this.CastTo(Upgrade).bind_face),
            restricted=1,
            change_on_event=OnEvent.AttachedMove("This"),
        ),
        AbilityFactory.WhenUnitDefendAgainstAttack(
            AbilityType.Interrupt,
            "AttachedCharacter",
            senkon,
            against_who=Enemy,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
