from . import *

# * Zeus (heros) — OLYMPUS. CTR 2, ATQ 2, DEF 2. Main 4 / 15 PV.
# Skyfather's Tempest — Response: After you spend both [energy] and
# [lightning] resources to pay for an event, resolve the "Special" ability on
# that event and remove 1 threat from a scheme.
#
# LE COEUR DU PACK. Quatre cartes y repondent par son NOM (ze007 The Aegis,
# ze008 Thunderbolt, ze009 Skyfather : `AfterPlayerResolveAbility(...,
# ability_name=TEMPEST)`), d'ou le `.SetName(TEMPEST)`. L'obligation ze012
# l'interdit tant qu'elle est en jeu : c'est une CONDITION ici, pas une
# interception la-bas.
#
# Modele du declencheur : `WhenPlayerPlayCard` (play.py:260), qui porte
# `paid_resources` ; ho006 pour la forme. « both [energy] and [lightning] » :
# voir PaieEnergieEtEclair dans __init__ (un joker vaut l'une OU l'autre,
# jamais les deux). « resolve the Special » : ResoudreLeSpecialDe, qui rend
# aussi le Special donne par Skyfather. « remove 1 threat from a scheme » :
# cible `Scheme2`, comme 01060 For Justice.
#
# ⚠ Le filtre du paiement va dans `conditions`, jamais dans le corps : une
# Response est PROPOSEE au joueur avant que le corps ne tourne.

def GetAbilities() -> Sequence['Ability']:

    def a_paye_energie_et_eclair(effect: 'Effect', message: 'Message.WhenPlayerPlayCard') -> bool:
        return PaieEnergieEtEclair(message.paid_resources)

    def sans_alcohol_problems(effect: 'Effect', message: 'Message.WhenPlayerPlayCard') -> bool:
        return AlcoholProblemsDe(effect.GetInitiator(), effect) is None

    def tempest(effect: 'Effect', message: 'Message.WhenPlayerPlayCard') -> None:
        this = effect.this.CastTo(Hero)
        initiator = effect.GetInitiator()
        ResoudreLeSpecialDe(message.played_face, initiator, effect)
        this.RemoveThreatFromSchemes(effect.targets, 1, effect)

    return [
        AbilityFactory.WhenPlayerPlayCard(
            AbilityType.Response,
            "You",
            CardFinder(card_type=Event),
            tempest,
            conditions=[a_paye_energie_et_eclair, sans_alcohol_problems],
        ).SetTarget(Scheme2)
        .SetName(TEMPEST),
    ]
