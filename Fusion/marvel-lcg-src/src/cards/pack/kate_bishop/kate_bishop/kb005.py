from . import *

# Quick Draw
# Alter-Ego Action: Flip to hero form and ready your hero.
# Hero Action: Ready your hero and place 2 arrow counters on Kate's Bow.
#
# Deux abilities distinctes (une par forme), modele Munitions Bunker
# (warm/war_machine/23003.py) et Unbelievable Gwenpool (gwenpool/gp009.py) :
# `AbilityType.AlterEgoAction` / `AbilityType.HeroAction` restreignent chacune
# a la forme correspondante sans verification manuelle. « Ready your hero » :
# `.SetTarget("YourHero")` + `Faces.ReadyAll(effect.targets, effect)`, modele
# "Fight Me, Coward!" (drax/19003.py).


def GetAbilities() -> Sequence['Ability']:

    def quick_draw_alter_ego(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()
        if initiator is None:
            return
        initiator.GetIdentity().ChangeToForm(Hero, effect)
        Faces.ReadyAll([initiator.GetIdentity()], effect)

    def quick_draw_hero(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        Faces.ReadyAll(effect.targets, effect)
        PlacerCompteursFlecheSurArc(effect, 2)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            quick_draw_alter_ego,
        ).SetPlay(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            quick_draw_hero,
        ).SetPlay().SetLabel()
        .SetTarget("YourHero"),
    ]
