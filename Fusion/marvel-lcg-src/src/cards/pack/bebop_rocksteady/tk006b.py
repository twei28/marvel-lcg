from . import *

# Gone Berserk! (face FERAL de Destructive Dunderheads)
# Permanent (desc). « Attach to the villain » : fait par tk006a, qui retourne la carte
# puis l'accroche au vilain restant. Crisis / Amplify / Hazard : lus dans desc.

def GetAbilities() -> Sequence['Ability']:

    # Regle de la partie, pas un texte imprime : le dernier vilain vaincu fait gagner les
    # joueurs. Le moteur ne le voit pas (le premier vilain vaincu est MIS DE COTE, donc la
    # zone « de cote » contient encore un vilain), et tk006a, retournee, ne ronde plus.
    def dernier_vilain_vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        Worlds.SetGameOver(True, effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.NonKeyword, "AttachedEnemy", dernier_vilain_vaincu),
        AbilityFactory.UnitCannotBeConfused(CardFinder(card_type=Villain)),
        *AbilityFactory.GiveKeywordToAttached(
            Villain,
            health=lambda effect: 12 * Worlds.GetPlayerNum(effect)),
    ]
