from . import *

# "It Can't End Like This!" — custom « ekAugust »
# Hero Action (attack/thwart): Deal 1 damage to the villain and remove 1
# threat from the main scheme. If the villain schemed last round, ____.
# Bulle : « Confuse the villain. »
# CORRECTIF (30/08/2026) : la carte porte les DEUX labels imprimes. Le module
# n'en posait qu'un, au motif que « le moteur n'accepte qu'un seul label » —
# c'est faux, `Ability.SetLabel(*labels)` est variadique et la carte OFFICIELLE
# 18004 Crosscounter en pose trois. Le label 'thwart' est ce qui declenche le
# statut Desoriente (`cards/pack/status/confused.py`) : sans lui, une Gwenpool
# Desorientee jouait cette carte, retirait quand meme sa menace, et GARDAIT son
# statut.

def GetAbilities() -> Sequence['Ability']:

    def it_cant_end_like_this(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        villain = Worlds.FindVillain(effect)
        if villain:
            this.DealDamage([villain], 1, effect)
        this.RemoveThreatFromSchemes("MainScheme", 1, effect)

        if VillainSchemedLastRound(effect):
            ResolveBlank(effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            it_cant_end_like_this
        ).SetPlay().SetLabel('attack', 'thwart'),
    ]
