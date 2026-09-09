from . import *

# Dive into Danger — EVENEMENT, cout 1, RES [mental]. THWART.
# Hero Action (thwart): Remove threat from a scheme equal to your THW and DEF
#   combined.
#
# CARTES DE REFERENCE
#  - `16003` "I am Groot" : « remove threat from a scheme equal to X », le
#    montage d'un retrait a valeur calculee.
#  - `29017` Go All Out : la SOMME de deux caracteristiques du heros, lue sur
#    `initiator.GetHero()`.
#
# TEXTE CONTRE CODE
#  ⚠ « YOUR THW and DEF » : les valeurs du HEROS, modificateurs compris
#    (`hero.thwart`, `hero.defense` sont les proprietes calculees, pas les
#    valeurs imprimees). Une amelioration posee compte donc, ce que le texte
#    veut dire par « your ».
def GetAbilities() -> Sequence['Ability']:

    def dive_into_danger(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        heros = effect.GetInitiator().GetHero()
        this.RemoveThreatFromSchemes(effect.targets, heros.thwart + heros.defense, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            dive_into_danger
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
