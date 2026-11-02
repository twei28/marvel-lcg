from . import *

# White Queen (sbire DIAMOND, module Perfection). Elite, Toughness (desc). « [star] Forced Response : After White Queen attacks and damages a character,
# stun that character. Forced Interrupt : When a White Queen minion attempts to enter play, give the engaged player a facedown encounter card and
# discard this card. » Cartes de reference : 22028 Gamora (`AfterUnitAttackAndDamageUnit`, `WhenCardWouldEnterPlay`), 41029 (statut).


def GetAbilities() -> Sequence['Ability']:
    def etourdir(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        Faces.GiveStatus([message.attacked], "Stunned", effect)

    return [
        AbilityFactory.AfterUnitAttackAndDamageUnit(AbilityType.ForcedResponse, "This", CardFinder(card_type=Hero | AlterEgo | Ally), etourdir),
        SbireWQEntreEnJeu(),
    ]
