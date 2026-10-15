from . import *

# Changing Appearance — ATTACHEMENT x2 (Skrull Elite - Skymax). CONDITION. +2 MNG, 2 icones de boost.
# Attach to a SKRULL minion. If you cannot, attach to the villain.
# Attached enemy cannot be attacked.
# Forced Interrupt: When attached enemy would attack, it schemes instead. Then, discard this card.
#
# Cartes de reference :
#  - Attache : helper `AttacherAUnSbireSkrull` (modele 01100 / sk146).
#  - « cannot be attacked » : **`ip034`** / `27152` (`UnitCannotBeAttacked(<qui>)`) avec `"AttachedEnemy"`.
#  - « would attack, it schemes instead » : **`sk099`** Intelligentsia / `40146` (`WhenUnitWouldAttack(
#    ForcedInterrupt, ..., message.DoSchemeInstead(effect))`), attaquant `"AttachedEnemy"`.
#  - +2 MNG : natif (`SCH+` du desc).
#
# ⚠ Mots-pieges : « attached ENEMY » (sbire ou mechant) ; « cannot be ATTACKED » (les joueurs ne peuvent plus
# l'attaquer ; ses propres attaques ne sont pas visees) ; « WOULD attack » (Interruption : l'attaque n'a
# pas lieu, il complote a la place) ; « Then, discard THIS card » : l'attachement part apres le complot ;
# une attaque lancee par un EFFET (pas une activation) est remplacee de meme, c'est le texte.


def GetAbilities() -> Sequence['Ability']:

    def complote(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this
        message.DoSchemeInstead(effect)
        Faces.DiscardAll([this], effect)

    return [
        AttacherAUnSbireSkrull(),
        AbilityFactory.UnitCannotBeAttacked("AttachedEnemy"),
        AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, "AttachedEnemy", complote),
    ]
