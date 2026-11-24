from . import *

# Shield Block — EVENEMENT, cout 0, [mental]. DEFENSE.
# Hero Interrupt (defense): When an identity would take any amount of damage, exhaust Captain America's Shield →
#   prevent all of that damage.
#
# CARTES DE REFERENCE
#  - `03005` Shield Block (Captain America officiel) : le meme cout (`CostFunc.Exhaust(card_type=Upgrade, name=..)`) et la meme
#    prevention totale ; seule la cible change (« you » -> « an identity »).
#  - `sr006` Webbed Up : le selecteur `Identity` de `WhenUnitWouldTakeDamage` pour « an identity ».
#
# TEXTE CONTRE CODE
#  « an identity » -> `Identity` (n'importe quelle identite, pas seulement la tienne ; en multijoueur elle protege un autre joueur).
#  « any amount of damage » -> PAS de `is_from_attack` : toute source de degats.
#  « exhaust Captain America's Shield » -> le bouclier que TU controles (`YouControlCards`), pas celui d'un autre joueur.
#  « Hero Interrupt » -> `HeroInterrupt` + `hero_form_only=True` (comme sr006).
#  « prevent all of that damage » -> `PreventDamage("All", ..)`.


def GetAbilities() -> Sequence['Ability']:

    def shield_block(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        message.PreventDamage("All", effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            Identity,
            shield_block,
        ).SetPlay(hero_form_only=True).SetLabel('defense')
        .SetCostFunc(CostFunc.Exhaust(card_type=Upgrade, name=NOM_BOUCLIER, from_where=["YouControlCards"])),
    ]
