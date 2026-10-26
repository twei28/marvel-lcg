from . import *
def GetAbilities() -> Sequence['Ability']:
    def retaliate_si_abime(effect: 'Effect', attach: Any, ui: List['CardFace']) -> int:
        return 1 if getattr(attach, "sustained", 0) >= SEUIL_DEGATS else 0
    return [
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            control_additional_restricted=CardFinder(card_type=Upgrade),
        ),
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            get_new_value=retaliate_si_abime,
            retaliate=1,
            ex_change_on_event=OnEvent.Health("YourIdentity"),
        ),
    ]
