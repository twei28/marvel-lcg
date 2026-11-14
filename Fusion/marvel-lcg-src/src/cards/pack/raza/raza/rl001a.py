from . import *
def GetAbilities() -> Sequence['Ability']:
    def augmentations(effect: 'Effect', ui: List['CardFace']) -> int:
        faces = AmeliorationsTechOuArme(JoueurDe(effect))
        ui.extend(faces)
        return len(faces)
    return [
        AbilityFactory.ThisGainKeyword(
            augmentations,
            health=1,
            change_on_event=OnEvent.AttachedMove(Upgrade),
        ),
    ]
