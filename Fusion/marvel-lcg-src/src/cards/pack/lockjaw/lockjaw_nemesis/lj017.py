from . import *

# Provoked — custom « Nugget » (némésis de Lockjaw)
# Attach to your identity card.  (-1 ATK : clé desc « ATK+ », native)
# Attached character cannot change to alter-ego form.
# [star] Response: After attached character attacks, place 1 calm counter here.
# Forced Interrupt: When there are 3 or more calm counters here, discard this
#   card.


def GetAbilities() -> Sequence['Ability']:

    def apres_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Attachment)
        Faces.PlaceCountersOn([this], 1, 'calm', effect)

        if this.CastTo(CanPlaceCounter).GetCounters('calm') >= 3:
            Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            "YourIdentity",
        ),
        AbilityFactory.PlayersCannotChangeForms(
            AbilityType.NonKeyword,
            "You",
            to_form=AlterEgo,
        ),
        AbilityFactory.AfterUnitAttackUnit(
            AbilityType.ForcedResponse,
            "AttachedIdentity",
            None,
            apres_attaque,
        ),
    ]
