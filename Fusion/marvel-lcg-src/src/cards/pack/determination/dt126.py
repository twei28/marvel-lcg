from . import *

# * Rage

def GetAbilities() -> Sequence['Ability']:

    def etape_du_vilain(effect: 'Effect', ui: List['CardFace']) -> int:
        villain = Worlds.FindVillain(effect)
        if villain is None:
            return 0
        ui.append(villain)
        return villain.printed_stage

    return [
        AbilityFactory.CardsEnterPlayExhausted("This"),
        AbilityFactory.ThisGainKeyword(
            etape_du_vilain,
            attack=1,
            change_on_event=OnEvent.GameArea(),
        ),
    ]
