from . import *

# Shield Strike
# Play only if Red Guardian's Shield is in your hand.
# Hero Action (attack): Deal 5 damage to an enemy. This attack gains piercing.
#
# Montage officiel identique : Superdense Strike (26009, Vision) — meme cout,
# meme 5 degats perforants, seule la condition de jeu change. Le mot-cle
# piercing n'est pas un keyword a donner, c'est une propriete de l'attaque :
# `property=AttackProperty(piercing=True)` sur `DealDamage` (cf. aussi Piercing
# Strike 04044).
#
# Le bouclier reste en main : la carte le demande comme condition, elle ne le
# depense pas.


def GetAbilities() -> Sequence['Ability']:

    def shield_strike(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        this.DealDamage(effect.targets, 5, effect,
                        property=AttackProperty(piercing=True))

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            shield_strike,
            conditions=[BouclierEstEnMain],
        ).SetPlay().SetLabel("attack")
        .SetTarget(Enemy),
    ]
