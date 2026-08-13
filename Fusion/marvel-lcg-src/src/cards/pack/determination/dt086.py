from . import *

# Aggressively Disarmed

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            "Players"
        ),
        *AbilityFactory.GiveKeywordToAttached(
            Hero,
            get_new_value=lambda effect, attach, ui:
                attach.health < attach.starting_health/2,
            attack=2,
            hand_size=-1,
            ex_change_on_event=OnEvent.Health("AttachedHero")
        ),
    ]
