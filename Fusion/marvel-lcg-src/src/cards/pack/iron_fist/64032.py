from . import *

# Sensei — AMELIORATION 2★ [physical], aspect Leadership (Iron Fist 32). TITLE.
# [star] Discount 2 (Martial Artist).
# Max 1 per player.
# Each Martial Artist ally you control takes −2 consequential damage (✪) after they exactly defeat an enemy or side scheme.
#
# MOTS-CLES : discount.md (fiche lue).
#
# CARTES DE REFERENCE
#  - `32091` Cannonball : reduction apres avoir vaincu un ennemi (`AfterUnitAttackAndDefeatUnit` + `GainForThisActive(
#    ..., message.GetWouldAtkMessage(), attack_consequential_damage=-N)`), `has_excess_damage=False` = « exactly »
#    (`ua019`, `pu026`).
#  - `40022` Uncanny X-Force : la meme reduction cote THWART apres une manigance annexe (`AfterUnitThwartScheme` +
#    `message.would_thw_message`, `thwart_consequential_damage=-N`) ; « exactly » = `scheme.excedent_de_menace == 0`
#    (champ pose par le moteur, `pu026`).
#
# TEXTE CONTRE CODE
#  ⚠ « EACH Martial Artist ALLY YOU CONTROL » : tout allie au trait, controle par le porteur de Sensei ; pas l'identite.
#  ⚠ « EXACTLY defeat » : sans exces (degats pour un ennemi, menace pour une annexe) ; un coup excedentaire ne reduit rien.
#  ⚠ « an enemy OR SIDE SCHEME » : l'attaque (ATK) ET la parade a la menace (THW) ont chacune leur reduction de −2.
#  ⚠ « after they ... defeat » : reduction au moment de la victoire ; sans victoire, les degats consecutifs restent.


def GetAbilities() -> Sequence['Ability']:

    def allie_artiste_martial_a_moi(effect: 'Effect', allie: 'CardFace|None') -> bool:
        if allie is None or not Ally.IsType(allie) or not allie.HasTrait("MARTIAL ARTIST"):
            return False
        return allie.GetControlByPlayer() == effect.this.GetControlByOrOwner()

    def apres_ennemi(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        message.killer.CastTo(Ally).GainForThisActive(effect, message.GetWouldAtkMessage(), attack_consequential_damage=-2)

    def apres_annexe(effect: 'Effect', message: 'Message.AfterUnitThwartScheme') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        message.trigger.CastTo(Ally).GainForThisActive(effect, message.would_thw_message, thwart_consequential_damage=-2)

    def ennemi_ok(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> bool:
        return allie_artiste_martial_a_moi(effect, message.killer)

    def annexe_ok(effect: 'Effect', message: 'Message.AfterUnitThwartScheme') -> bool:
        scheme = message.scheme
        return allie_artiste_martial_a_moi(effect, message.trigger) and scheme.threat == 0 and \
            getattr(scheme, 'excedent_de_menace', 0) == 0

    return [
        DiscountAbility(2, ['MARTIAL ARTIST']),
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.AfterUnitAttackAndDefeatUnit(
            AbilityType.NonKeyword,
            Ally,
            Enemy,
            apres_ennemi,
            has_excess_damage=False,
            conditions=[ennemi_ok],
        ),
        AbilityFactory.AfterUnitThwartScheme(
            AbilityType.NonKeyword,
            "YouControlAlly",
            SchemeSide2,
            apres_annexe,
            conditions=[annexe_ok],
        ),
    ]
