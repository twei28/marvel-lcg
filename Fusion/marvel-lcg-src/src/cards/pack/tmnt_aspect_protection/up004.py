from . import *

# Autodefenestration — EVENEMENT 0* [physical], aspect Protection (TMNT Aspects, Inkwire). DEFENSE. FERAL. NYC.
# [star] Rampage 2. (As an additional cost for this card, take 2 damage and discard 2 cards from the top
#   of your deck.)
# Hero Interrupt (defense): When you would take any amount of damage from an attack, prevent all of that
#   damage.
#
# MODIFIEE de `01003` Backflip (carte heros de Spider-Man) : Rampage 2 ajoute, « Hero Interrupt » au lieu
# de « Interrupt », aspect Protection. Script propre (pas d'ability_link).
#
# MOT-CLE (fiche lue AVANT le code) : RAMPAGE X — docs/reference/mots-cles/rampage.md. `CostFunc.Rampage(2)`
# sur la capacite de JEU de l'evenement (ici l'interruption de heros). Le « 0* » et le [star] = rappel.
#
# CARTES DE REFERENCE
#  - `01003` Backflip : `WhenUnitWouldTakeDamage(..., "You", is_from_attack=True)` + `PreventDamage("All")`.
#  - `ua015` Demolish : `.SetCostFunc(CostFunc.Rampage(X))` sur la capacite jouee.
#  - `21061` Shield Spell : meme fenetre en `AbilityType.HeroInterrupt` avec un cout additionnel.
#
# TEXTE CONTRE CODE
#  ⚠ « Hero Interrupt » : `AbilityType.HeroInterrupt` (forme heros), pas `Interrupt` comme Backflip.
#  ⚠ « When YOU would take ... damage FROM AN ATTACK » : l'identite du joueur, `is_from_attack=True`.
#  ⚠ « prevent ALL of that damage » : `PreventDamage("All")`.
#  ⚠ Rampage 2 = cout : 2 degats a l'identite PUIS 2 cartes du deck ; payes AVANT la prevention (les 2
#    degats du cout ne sont pas « d'une attaque », ils ne se previennent pas eux-memes).


def GetAbilities() -> Sequence['Ability']:

    def autodefenestration(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        message.PreventDamage("All", effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            autodefenestration,
            is_from_attack=True,
        ).SetPlay().SetLabel('defense')
        .SetCostFunc(CostFunc.Rampage(2)),
    ]
