from . import *

# * Hera (allie, cout 2, CTR 2*, ATQ 1*, 2 PV, joker)
# Response: After Hera enters play, choose a card in your hand with a printed
# "Special" ability, then resolve that ability.
#
# Modele du declencheur : 01083 Mockingbird (AfterCardEnterPlay). Le choix se
# fait dans la MAIN, sur un Special IMPRIME (voir APrintedSpecial dans
# __init__ : on lit les capacites DECLAREES, pas les effets enregistres, car
# une carte en main n'est pas en jeu). Skyfather ne compte pas ici : son
# Special est donne, pas imprime.
#
# ⚠ Le filtre « au moins une carte candidate » va dans `conditions`, jamais
# dans le corps : une Response est PROPOSEE au joueur avant que le corps ne
# tourne (RECETTES-MOTEUR §1).

def GetAbilities() -> Sequence['Ability']:

    def candidates(effect: 'Effect') -> List['CardFace']:
        initiator = effect.GetInitiator()
        return [face for face in initiator.hand_cards.Get() if APrintedSpecial(face)]

    def a_une_candidate(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> bool:
        return candidates(effect) != []

    def hera(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)
        initiator = effect.GetInitiator()
        cartes = candidates(effect)
        if not cartes:
            return
        choisie = initiator.AskChooseFace(cartes, effect)
        if choisie:
            ResoudreLeSpecialDe(choisie, initiator, effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            hera,
            conditions=[a_une_candidate],
        ),
    ]
