from . import *

# Kree Ferocity — evenement signature x2 (5/16, 6/16). KREE. SUPERPOWER.
# Cout 2 [physical].
# Hero Interrupt: When you make a basic attack, you get +6 ATK for that attack.
#   You may take 2 indirect damage → that attack gains overkill.
#
# Cartes de reference :
#  - **`56017`** Savage Strike / `ah011` Kinetic Stomp : « When you make a basic
#    attack, you get +6 ATK for that attack » :
#    `WhenUnitMakeAttack(HeroInterrupt, "You", op, is_basic_attack=True)` +
#    `message.GainATKForThisAttack(6, effect)`.
#  - **`10003`** Hulk Smash / `32007` Made of Rage : `message.GainOverKill(effect)`.
#  - **`32008`** Steel Fist : « You may <cout> → <bonus> » DANS l'effet,
#    `MayChooseOneAbility(effect, ForChoiceAbility3(...))`.
#  - `mf017` / `ra028` : `identite.TakeIndirectDamage(source, 2, effect)`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **basic** attack » : `is_basic_attack=True`.
#  - « +6 ATK » : chiffre verifie sur le scan le 15/10/2026 (inhabituel mais
#    imprime, comme Savage Strike et Kinetic Stomp).
#  - « You **may** take 2 **indirect** damage → » : optionnel ; INDIRECTS =
#    le joueur les repartit entre son identite et ses allies
#    (`TakeIndirectDamage`, can_health.py). Le +6 tombe dans tous les cas.
#  - Pas d'etiquette imprimee (pas « (attack) ») : `SetLabel()` vide, comme
#    Savage Strike.


def GetAbilities() -> Sequence['Ability']:

    def ferocite(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Event)

        message.GainATKForThisAttack(6, effect)

        joueur = effect.GetInitiator()

        def surcharge(targets: Sequence['CardFace'], by_effect: 'Effect') -> None:
            Unused(targets, by_effect)
            joueur.GetIdentity().TakeIndirectDamage(this, 2, effect)
            message.GainOverKill(effect)

        joueur.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility3(
                "Take 2 indirect damage: that attack gains overkill",
                surcharge,
            ),
        )

    return [
        AbilityFactory.WhenUnitMakeAttack(
            AbilityType.HeroInterrupt,
            "You",
            ferocite,
            is_basic_attack=True,
        ).SetPlay().SetLabel(),
    ]
