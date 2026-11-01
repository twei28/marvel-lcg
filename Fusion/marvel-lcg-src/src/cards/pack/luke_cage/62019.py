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
            # Sans cet evenement le bonus n'etait recalcule qu'a l'entree en jeu d'une carte : un allie qui TOMBE a 1 PV apres la pose ne le recevait
            # pas (signale en partie reelle le 01/11/2026, cas `[nd]`).
            change_on_event=OnEvent.Health(Unit2),
        ),
    ]
