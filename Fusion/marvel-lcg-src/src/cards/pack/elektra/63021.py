from . import *

# Shuriken — AMELIORATION 2★ [energy], aspect Aggression (Elektra Natchios 21). WEAPON.
# [star] Discount 1 (Martial Artist).
# Uses (3 shuriken counters).
# Hero Action: Remove 1 shuriken counter from here → deal 1 damage to an enemy.
#
# MOTS-CLES (fiches lues) : discount.md (`DiscountAbility`, desc.Cost garde l'etoile) ; Uses = `desc.Uses "3,shuriken"` (compteur
# `shuriken` declare dans `CardFace.COUNTER`), aucun code.
#
# CARTES DE REFERENCE
#  - `64017` The Night Nurse (ex-`09019`) : `Uses (3 ... counters)` + « Remove 1 counter from here → » = `CostFunc.Counter("This", 1, '<compteur>')`.
#  - `64032`/`60027` : `DiscountAbility` + `CanPlayThisUpgradeCard()` (amelioration posee sur son propre porteur).
#  - `ua040` Ujigami : « deal 1 damage to an enemy » = `this.DealDamage(effect.targets, 1, effect)` avec `.SetTarget(Enemy)`.
#
# TEXTE CONTRE CODE
#  ⚠ « Hero Action » SANS (attack) : 1 degat de carte, PAS une attaque (aucune etiquette, aucun bonus d'ATQ).
#  ⚠ « Remove 1 shuriken counter » : cout, une fois les 3 retires la carte reste en jeu sans compteur (rien ne la defausse).
#  ⚠ « Hero » : forme heros seulement (pas d'Action en alter ego).


def GetAbilities() -> Sequence['Ability']:

    def shuriken(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        this.DealDamage(effect.targets, 1, effect)

    return [
        DiscountAbility(1, ['MARTIAL ARTIST']),
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            shuriken,
        ).SetCostFunc(CostFunc.Counter("This", 1, 'shuriken')).SetTarget(Enemy),
    ]
