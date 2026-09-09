from . import *

# "You Are What You Eat" — AMELIORATION, cout 0, RES [physical]. SUPERPOWER.
# Max 1 per player.
# Response: After you heal damage from your identity, exhaust this card ->
#   draw 1 card.
#
# CARTE DE REFERENCE
#  - `vr014` * Carnage (pack venom_rainy, meme famille symbiote) : « Forced
#    Response: After you heal damage, take 1 damage. » AUCUNE FABRIQUE
#    n'expose la fenetre de soin — l'Ability est construite A LA MAIN sur
#    `Message.AfterUnitHealHealth`, comme le font `vr014` et `th001b`. On
#    reprend ce montage.
#
# TEXTE CONTRE CODE
#  ⚠ « from YOUR IDENTITY » : la condition compare `message.trigger` a
#    l'identite du joueur qui controle cette carte. Sans elle, le soin d'un
#    ALLIE ou d'un autre joueur ferait piocher, ce que la carte ne dit pas.
#  ⚠ « exhaust this card » est le COUT -> `SetCostFunc`. Une carte deja
#    inclinee ne pioche pas : c'est la seule limite de la carte, elle n'a pas
#    de « Limit once per round ».
def GetAbilities() -> Sequence['Ability']:

    def le_soin_va_a_mon_identite(effect: 'Effect', message: 'Message.AfterUnitHealHealth') -> bool:
        joueur = effect.this.GetControlByOrOwner()
        if not Player.IsType(joueur):
            return False
        return message.trigger == joueur.GetIdentity()

    def you_are_what_you_eat(effect: 'Effect', message: 'Message.AfterUnitHealHealth') -> None:
        Unused(message)
        joueur = effect.this.GetControlByOrOwner()
        if Player.IsType(joueur):
            joueur.DrawUp(1, effect)

    return [
        Ability(
            AbilityType.Response,
            Message.AfterUnitHealHealth,
            [le_soin_va_a_mon_identite],
            you_are_what_you_eat,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
