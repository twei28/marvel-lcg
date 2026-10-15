from . import *

# * Skrull Kill Krew — SOUTIEN de campagne (Aggression / Campaign, n° 282). Cout 2. CREW.
# Hero Action: Exhaust Skrull Kill Krew -> deal 1 damage to a SKRULL minion. If that minion is defeated this
#   way, ready Skrull Kill Krew.
#
# Cartes de reference :
#  - **`ho004`** : « for each enemy defeated this way » = `DealDamage(..., if_this_attack_defeats=fn)`.
#  - **`vnm/20022`** Plasma Pistol : « Hero Action: Exhaust X -> deal 1 damage to an enemy » =
#    `WhenInYourPlayTurn(HeroAction, op).SetCostFunc(CostFunc.Exhaust("This")).SetTarget(...)` + `this.DealDamage`.
#  - **`Faces.ReadyAll([this], effect)`** : redresser la carte (RECETTES §2, `an001a`).
#
# ⚠ Mots-pieges : « Hero Action » (forme heros seulement) ; « a SKRULL MINION » (jamais le mechant, meme
# SKRULL) ; « IF that minion is defeated THIS WAY » : seul l'achevement par CES degats redresse le soutien ;
# « ready Skrull Kill Krew » = il peut agir de nouveau (l'inclinaison etait le cout).


def GetAbilities() -> Sequence['Ability']:

    def kill_krew(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        vaincus: List['Unit2'] = []

        def vaincu(unit: 'Unit2') -> None:
            vaincus.append(unit)

        this.DealDamage(effect.targets, 1, effect, if_this_attack_defeats=vaincu)
        if vaincus:
            Faces.ReadyAll([this], effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            kill_krew,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Minion, trait="SKRULL"),
    ]
