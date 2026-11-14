from . import *

# * Boom Boom (Tabitha Smith) : allie Leadership, cout 4, PV 2, THW 1*, ATK 1*. X-FORCE.
# Response: After your turn begins, place 1 boom counter to Boom Boom (to a maximum of 5). Then, you may discard Boom Boom to deal 2
# damage to the villain for each boom counter.
#
# Cartes de reference : 43013 Boom Boom (officielle, compteurs boom), `Faces.PlaceCountersOn(..., maximum=5)` (faces.py:213),
# `joueur.ChooseAbilities(effect, ForChoiceAbility(...), forced=False)` (« you may », player_action.py:671).
# ⚠ « for each boom counter » : le nombre de compteurs AVANT la defausse (lu d'abord).
def GetAbilities() -> Sequence['Ability']:
    def boom(effect: 'Effect', message: 'Message.AfterPlayerTurnBegin') -> None:
        this = effect.this.CastTo(Ally)
        joueur = JoueurDe(effect)
        Faces.PlaceCountersOn([this], 1, 'boom', effect, maximum=5)
        nombre = this.GetCounters('boom')

        def detoner(targets: Sequence['CardFace']) -> None:
            Faces.DiscardAll([this], effect)
            this.DealDamage(targets, 2 * nombre, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Discard Boom Boom to deal 2 damage to the villain for each boom counter",
                detoner,
            ).SetTarget(Villain),
            forced=False,
        )

    return [
        AbilityFactory.AfterPlayerTurnBegin(
            AbilityType.Response,
            "You",
            boom,
        ),
    ]
