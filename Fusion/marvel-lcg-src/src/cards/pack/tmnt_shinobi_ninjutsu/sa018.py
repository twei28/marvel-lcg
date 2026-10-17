from . import *

# Smokescreen — AMELIORATION 1 [physical], Ninjutsu (TMNT Shinobi, Inkwire). PREPARATION.
# Reduce the cost to play this card by 1 if your identity is cloaked.
# Hero Interrupt (defense): When an enemy attack would deal damage to a friendly character, discard this card ->
# prevent 2 of that damage.
#
# NOUVELLE. Mots-cles (fiches lues AVANT le code) : Cloaked (cloaked.md).
#
# Cartes de reference :
#  - `up023` Lookout : amelioration PREPARATION sans « Attach to » = `CanPlayThisUpgradeCard()` + `ReduceCostToPlayThis(1,
#    conditions=[...])` + cout `CostFunc.Discard("This")` ;
#  - `04004` Autodefenestration / `Cloaked` (status/cloaked.py) : « prevent N of that damage » = `message.PreventDamage(
#    min(N, degats), effect)` sur `WhenUnitWouldTakeDamage(.., is_from_attack=True)`.
#
# TEXTE CONTRE CODE
#  ⚠ « if YOUR IDENTITY is cloaked » : l'identite (quelle que soit sa forme) porte une carte Cloaked ; cout reduit de 1
#    (jamais sous 0).
#  ⚠ « When an ENEMY attack would deal damage to a FRIENDLY character » : l'attaque d'un ennemi (vilain ou sbire), la
#    victime est une identite ou un allie (de n'importe quel joueur) : PAS une attaque d'allie ni un degat hors attaque ;
#    « prevent 2 OF THAT DAMAGE » : 2 au plus (tout si moins) ; « discard THIS card -> » est le COUT.
#  ⚠ Hero Interrupt (forme heros seulement) ; « (defense) » est le sous-type imprime (etiquette).


def GetAbilities() -> Sequence['Ability']:

    def identite_camouflee(effect: 'Effect', message: 'Message2') -> bool:
        Unused(message)
        return IdentiteCamouflee(effect.GetInitiator())

    def smokescreen(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        message.PreventDamage(min(2, message.will_take_damage), effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.ReduceCostToPlayThis(
            1,
            conditions=[identite_camouflee],
        ),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            Friend,
            smokescreen,
            is_from_attack=True,
            who_deal_damage=Enemy,
        ).SetLabel('defense')
        .SetCostFunc(CostFunc.Discard("This")),
    ]
