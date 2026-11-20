from . import *

# * She-Hulk (Ally, reecriture a 3 couts de l'original officiel 62021, pour la restriction de deck de 3-D Man)
#
# Play only if your identity has the AVENGER trait.
# Response: After you play a 3-cost event, deal 1 damage to an enemy.
#
# CARTES DE REFERENCE
#  - `16047` Groot : "Play only if your identity has the <TRAIT> trait" -> `AbilityFactory.CanPlayThisAllyCard()
#    .SetPlay(only_if_your_identity_has_trait="AVENGER")`.
#  - `play.py:363` `AfterPlayerPlayedCard(Response, "You", CardFinder(card_type=Event), op)` : "after you play an
#    event". Le filtre de COUT ("a 3-cost event") n'a pas de parametre dedie dans `CardFinder` -> condition
#    separee sur `message.played_face.printed_cost.val == 3` (attribut standard, lu sur la carte REELLEMENT
#    jouee, pas une valeur devinee).
#
# TEXTE CONTRE CODE
#  "a 3-cost EVENT" : Event ET cout imprime exactement 3 (deux filtres, l'un sur le type via CardFinder, l'autre
#    sur le cout imprime en condition).
#  "deal 1 damage to an enemy" : un seul ennemi choisi par le joueur (pas "each enemy").

def GetAbilities() -> Sequence['Ability']:

    def evenement_a_3_couts(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> bool:
        return message.played_face.printed_cost.val == 3

    def she_hulk(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Ally)
        this.DealDamage(effect.targets, 1, effect)

    return [
        AbilityFactory.CanPlayThisAllyCard().SetPlay(only_if_your_identity_has_trait="AVENGER"),
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Response,
            "You",
            CardFinder(card_type=Event),
            she_hulk,
            conditions=[evenement_a_3_couts],
        ).SetTarget(Enemy),
    ]
