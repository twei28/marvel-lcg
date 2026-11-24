from . import *
def GetAbilities() -> Sequence['Ability']:
    def bonus_atk(effect: 'Effect', attach: Any, ui: List['CardFace']) -> int:
        return 2 if getattr(attach, "sustained", 0) >= SEUIL_DEGATS else 1
    return [
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            get_new_value=bonus_atk,
            attack=1,
            ex_change_on_event=OnEvent.Health("YourIdentity"),
        ),
    ]
