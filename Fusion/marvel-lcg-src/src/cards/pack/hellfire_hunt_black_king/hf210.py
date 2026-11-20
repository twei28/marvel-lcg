from . import *

# Surge (Noriko Ashida), allie CAPTIVE MUTANT. « [star] Interrupt : When Surge attacks an enemy, that enemy get stunned. »
# Cartes de reference : hf208 (`WhenUnitWouldAttack(Interrupt, "This", op)`), 01083 / 05015 (`Faces.GiveStatus(cibles, "Stunned", effect)`).
# ⚠ « attacks an ENEMY » : les cibles de l'attaque qui sont des ennemis ; l'Interruption est au CHOIX du joueur (Interrupt, pas Forced).


def GetAbilities() -> Sequence['Ability']:
    def surge(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        ennemis = [f for f in message.attacked_targets if Enemy.IsType(f)]
        Faces.GiveStatus(ennemis, "Stunned", effect)

    return [AbilityFactory.WhenUnitWouldAttack(AbilityType.Interrupt, "This", surge), CaptifRecrute()]
