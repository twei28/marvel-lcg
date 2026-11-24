from . import *

# Newhaven — PLAYER ENVIRONMENT. PLANET. Planet deck (3/5).
#
# Texte imprime :
#  « Arrive: The arriving character gains +2 THW until the end of the
#    round. »
#  « Depart: Remove 2 threat from a scheme. »
#
# CARTES DE REFERENCE : voir pc005 Sakaar (meme gabarit). `01084` Nick Fury :
# `initiator.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility(...)
# .SetTarget(Scheme2))` — PAS un `.SetTarget()` pose directement sur
# l'Ability reactive elle-meme : mesure le 05/11/2026, `effect.targets`
# restait VIDE avec cette seconde forme sur un message maison
# (`AfterCharacterDepartPlanet`), silencieusement (`if not effect.targets:
# return`), alors que `ChooseAbilities`/`ForChoiceAbility` fonctionne.


def GetAbilities() -> Sequence['Ability']:

    def ici(effect: 'Effect', message: 'Message.AfterCharacterArrivePlanet|Message.AfterCharacterDepartPlanet') -> bool:
        return effect.this == message.planet_face

    def arrivee(effect: 'Effect', message: 'Message.AfterCharacterArrivePlanet') -> None:
        message.character_face.GainUntilRoundEnd(effect, thwart=2)

    def depart(effect: 'Effect', message: 'Message.AfterCharacterDepartPlanet') -> None:
        Unused(message)
        this = effect.this
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return

        def retirer_menace(cibles: Sequence['CardFace']) -> None:
            this.RemoveThreatFromSchemes(cibles, 2, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Remove 2 threat from a scheme",
                retirer_menace,
            ).SetTarget(Scheme2),
        )

    return [
        Ability(AbilityType.Response, Message.AfterCharacterArrivePlanet, [ici], arrivee),
        Ability(AbilityType.Response, Message.AfterCharacterDepartPlanet, [ici], depart),
    ]
