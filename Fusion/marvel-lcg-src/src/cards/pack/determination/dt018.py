from . import *

# Feel the Pain

def GetAbilities() -> Sequence['Ability']:

    # La carte dit « maximum hit points », pas « starting » : c'est `max_health`,
    # qui compte les points gagnes en jeu, la ou `starting_health` s'en tient a
    # l'imprime. Le jumeau officiel 43019 dit « starting » et lit l'autre.
    return [
        *AbilityFactory.GiveKeywordToAttached(
            Hero,
            get_new_value=lambda effect, attach, ui:
                attach.health < attach.max_health/2,
            retaliate=1,
            ex_change_on_event=OnEvent.Health("AttachedHero")
        ),
    ]
