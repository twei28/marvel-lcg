from . import *

# Iron Sight
#
# "Usage (2 per_hero jetons Observation)" = desc.Uses="2*,observation" (le
# suffixe * = par joueur, meme convention que Hinder). Annulation des icones
# de boost modele Foiled! (drs/09038.py) : `WhenBoostCardTurnedFaceUp` +
# `message.CancelAllBoostIcons(effect)`, sans restriction `while_scheme`
# puisque le texte dit "durant une activation" (n'importe laquelle).
#
# CORRECTIF (meme bug que si002) : PAS de `.SetPlay()`. Foiled! est un
# Event que l'on joue depuis la main (`.SetPlay()` y est juste), Iron Sight
# est un Support DEJA en jeu : `.SetPlay()` marque l'ability `func_name=
# "Play"` (ability.py:613), et `Support.GetAbilities()` (card_type/
# support.py) ne cree alors PLUS le `CanPlayThisSupportCard()` par defaut
# puisqu'il en trouve deja une portant ce nom -- la carte devient injouable
# depuis la main.

def GetAbilities() -> Sequence['Ability']:

    def iron_sight(effect: 'Effect', message: 'Message.WhenBoostCardTurnedFaceUp') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)
        message.CancelAllBoostIcons(effect)

    return [
        AbilityFactory.WhenBoostCardTurnedFaceUp(
            AbilityType.Interrupt,
            "BoostIcons",
            iron_sight,
        ).SetLabel()
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'observation')),
    ]
