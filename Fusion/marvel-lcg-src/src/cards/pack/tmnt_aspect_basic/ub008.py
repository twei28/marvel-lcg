from . import *

# * Donatello « Donnie » — ALLIE 3 [mental], 2**/2**, 2 PV, aspect Basic (TMNT Aspects). GENIUS. NINJA. TURTLE.
# Response: After Donatello enters play, draw 2 cards.
#
# NOUVELLE. Cartes de reference : 45048 Triage (declencheur « After X enters play » =
# `AfterCardEnterPlay(Response, "This")`) ; 01084 Nick Fury (« draw 3 cards » = `initiator.DrawUp(N)`).
# TEXTE CONTRE CODE : « enters play » (pas seulement « play from hand » : une mise en jeu par effet compte) ;
# « draw 2 » : le joueur qui le controle. Les deux icones de degat consecutif (2**) sont dans `desc`.


def GetAbilities() -> Sequence['Ability']:

    def donatello(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        effect.GetInitiator().DrawUp(2, effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            donatello
        ),
    ]
