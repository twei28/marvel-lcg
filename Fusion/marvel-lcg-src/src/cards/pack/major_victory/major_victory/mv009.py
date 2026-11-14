from . import *

# Victory's Command — EVENEMENT, cout 1, [physical]. TACTIC.
# Hero Interrupt: When a friendly character makes a basic thwart or attack, exhaust Captain America's Shield →
#   they get +2 to that basic power for this use. Ready that character.
#
# CARTES DE REFERENCE
#  - `49019` « You Got This! » : `WhenUnitUseBasicPower` avec `powers=["THW","ATK"]` (UNE seule capacite Play pour attaque
#    ET thwart, pas besoin de la liste blanche de la fabrique) + `Faces.ReadyAll([message.trigger], ..)`.
#  - `03005` : le cout « exhaust Captain America's Shield ».
#  - `GainValue` (sender_unit.py) : ajoute au pouvoir de base utilise, quel qu'il soit (ATK ou THW).
#
# TEXTE CONTRE CODE
#  « a friendly character » -> `Friend` (identite ET allies, de n'importe quel joueur), pas `YourHero`.
#  « basic thwart or attack » -> `powers=["THW","ATK"]` (ni DEF, ni REC, ni SCH).
#  « +2 to that basic power for this use » -> `message.GainValue(2, ..)`. Chiffre : 2.
#  « Ready that character » -> `message.trigger`, le personnage qui agit.
#  « Hero Interrupt » -> `HeroInterrupt`.


def GetAbilities() -> Sequence['Ability']:

    def victorys_command(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        message.GainValue(2, effect)
        Faces.ReadyAll([message.trigger], effect)

    return [
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.HeroInterrupt,
            Friend,
            victorys_command,
            powers=["THW", "ATK"],
        ).SetPlay().SetLabel()
        .SetCostFunc(CostFunc.Exhaust(card_type=Upgrade, name=NOM_BOUCLIER, from_where=["YouControlCards"])),
    ]
