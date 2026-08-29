from . import *
def GetAbilities() -> Sequence['Ability']:
    def righteous_purpose_value(effect: 'Effect', face: 'CardFace') -> int:
        return 1 if face.health == 1 else 0
    return [
        AbilityFactory.CanPlayThisSupportCard(under_any_players_control=True),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            Unit2,
            control_by="You",
            thwart=2,
            attack=2,
            get_new_value=righteous_purpose_value,
        ),
    ]
