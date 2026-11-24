from . import *

# The Power Cosmic — RESSOURCE ([wild]).
#
# Texte imprime : « Response: After you spend this card, shuffle it into
# your deck. Then, if you spent it on a POWER COSMIC or COSMIC card, draw
# 1. »
#
# CARTES DE REFERENCE
#  - `dy012` Fragment Studies (destiny) : `AbilityFactory.AfterYouSpendThisCard
#    (AbilityType.Response, op)` — modele exact du declencheur « after you
#    spend this card ».
#  - `message.pay_for_card` (sender_card.py, `AfterCardsBeSpendAsResource`) :
#    la carte PAYEE par cette ressource (None si la depense ne payait pas une
#    carte jouee, ex. un cout de capacite) -- c'est elle qu'on teste pour
#    « POWER COSMIC or COSMIC ».
#
# TEXTE CONTRE CODE
#  « shuffle IT into your deck » : toujours, meme si la carte payee n'avait
#    pas le bon trait (ce n'est que le TIRAGE qui est conditionnel).
#  « if you spent it on a POWER COSMIC OR COSMIC card » : `pay_for_card`
#    peut etre None (depense sur un cout de capacite, pas une carte jouee) :
#    alors pas de pioche.


def GetAbilities() -> Sequence['Ability']:

    def the_power_cosmic(effect: 'Effect', message: 'Message.AfterCardsBeSpendAsResource') -> None:
        this = effect.this
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        Faces.ShuffleAllTo([this], joueur.player_deck, effect)

        carte_payee = message.pay_for_card
        if carte_payee is not None and (carte_payee.HasTrait("POWER COSMIC") or carte_payee.HasTrait("COSMIC")):
            joueur.DrawUp(1, effect)

    return [
        AbilityFactory.AfterYouSpendThisCard(
            AbilityType.Response,
            the_power_cosmic,
        ),
    ]
