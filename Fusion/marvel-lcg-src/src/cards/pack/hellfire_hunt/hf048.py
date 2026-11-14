from . import *

# * Xavier's Institute (environnement de campagne, scenarios 1 a 4).
# Forced Response: After a RECRUITED ally is discarded, place it into the Recruited Mutants discard pile instead.
# Action: Spend 1 resource of any type -> draw 1 card from the Recruited Mutants deck. (Max once per phase per player.)
#
# Cartes de reference : `AbilityFactory.AfterCardDiscard` (discard.py) pour deplacer l'allie defausse, `RecruitedMutants` / `PiocherDesRecrutes`
# (__init__.py, E2), `LimitOncePerPhasePerPlayer`.
# ⚠ « instead » : l'allie PART de la defausse du joueur et ARRIVE dans la defausse Recruited (jamais dans les deux).
def GetAbilities() -> Sequence['Ability']:
    def vers_les_recrutes(effect: 'Effect', message: 'Message.AfterCardDiscard') -> None:
        _, defausse = RecruitedMutants(effect)
        face = message.trigger
        if face is not None and face.card.area is not defausse:
            Faces.MoveAllTo([face], defausse, effect)

    def piocher(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        joueur = effect.GetInitiator()
        PiocherDesRecrutes(effect, joueur)

    return [
        AbilityFactory.AfterCardDiscard(
            AbilityType.ForcedResponse,
            CardFinder(card_type=Ally, trait="RECRUITED"),
            vers_les_recrutes,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            piocher,
        ).SetCost(Cost("1")).LimitOncePerPhasePerPlayer(),
        *PermissionDeJouerLesRecrutes(),
    ]
