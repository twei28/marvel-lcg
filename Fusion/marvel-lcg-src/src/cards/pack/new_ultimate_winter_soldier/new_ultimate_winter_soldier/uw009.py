from . import *

# * Winter Mask — amelioration unique EARTH-6160. ITEM. Cout 2, [mental].
# Hero Response: After you discard a card from your hand at random, take 1 damage -> draw 1 card.
#
# Cartes de reference : `35012`/`27070` pour `CostFunc.TakeDamage(1, "Initiator")` + `DrawUp` (Focused Rage 01027, meme
# cout et meme effet) ; `40043`/`40060` (`AfterCardDiscardInternal`) pour le declencheur « after a card is discarded ».
# La mention « AT RANDOM » est lue sur la marque `world.defausses_au_hasard` (CORRECTIF `DiscardRandomHandCards`), la
# main du JOUEUR sur le proprietaire de la carte defaussee.
#
# Mots-pieges : « YOU discard » (la main du porteur, pas celle d'un autre joueur) ; « at random » (une defausse CHOISIE
# ne declenche rien) ; une Response FACULTATIVE dont le cout est des degats : chaque carte tiree au hasard la propose une
# fois ; « Hero » (forme heros seulement).


def GetAbilities() -> Sequence['Ability']:

    def winter_mask(effect: 'Effect', message: 'Message.AfterCardDiscard') -> None:
        initiator = effect.GetInitiator()
        initiator.DrawUp(1, effect)

    def defausse_de_ma_main_au_hasard(effect: 'Effect', message: 'Message.AfterCardDiscard') -> bool:
        return DefausseAuHasard(message) and message.trigger.GetOwnerPlayer() is effect.this.GetControlByPlayer()

    return [
        AbilityFactory.AfterCardDiscardInternal(
            AbilityType.HeroResponse,
            CardFinder(),
            winter_mask,
            conditions=[defausse_de_ma_main_au_hasard],
        ).SetCostFunc(CostFunc.TakeDamage(1, "Initiator")),
    ]
