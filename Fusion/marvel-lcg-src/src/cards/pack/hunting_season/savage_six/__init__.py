from cards.pack import *
from weakref import WeakKeyDictionary

TRAIT = "SAVAGE SIX"

# Memorise, pour une carte de rencontre en boost, si l'ancre de l'icone supplementaire est remplie.
_icone_en_plus: 'WeakKeyDictionary[CardFace, bool]' = WeakKeyDictionary()


def EstSavageSix(face: 'CardFace|None') -> bool:
    return face is not None and face.HasTrait(TRAIT)


def NoterIconeSi(face: 'CardFace', vrai: bool) -> None:
    _icone_en_plus[face] = vrai


def IconeEnPlus() -> 'Ability':
    """+1 icone de boost si le drapeau pose par le handler de boost est vrai."""
    def condition(effect: 'Effect', message: 'Message.WhenBoostIconsWouldBeCount') -> bool:
        return message.trigger is effect.this and _icone_en_plus.pop(effect.this, False)

    return AbilityFactory.IncreaseBoostIconsOnEncounterCard(conditions=[condition])


def BoostPourIconeSi(test: 'Callable[[Effect, Message.WhenCardBecomeBoost], bool]') -> 'Ability':
    def noter(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        NoterIconeSi(effect.this, test(effect, message))

    return AbilityFactory.WhenCardBecomeBoost("This", noter)


def MalusApresDegats(statut: str) -> 'Ability':
    """Forced Response : apres que ce serviteur attaque et blesse un personnage, ce personnage recoit le statut."""
    def donner(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        Faces.GiveStatus(list(message.damaged_targets), statut, effect)

    def blesse(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> bool:
        return len(message.damaged_targets) > 0

    return AbilityFactory.AfterUnitAttackEnd(AbilityType.ForcedResponse, "This", donner, conditions=[blesse])
