from . import *

# Astral Trap. Attachement ILLUSION PSIONIC. « Attach to your identity. Uses (1 illusion counter). Attached character cannot be healed. When Revealed :
# If the villain or a minion engaged with you has the PSIONIC trait, place 1 additional illusion counter here. Alter-Ego Action : Exhaust a character
# you control -> remove 1 illusion counter from here. » Cartes de reference : 90129 (soin remplace), 04136 Bitter Rival (`"YouControlUnit"`).


def GetAbilities() -> Sequence['Ability']:
    def action(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        RetirerUnCompteurIllusion(effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay("YourIdentity"),
        PoserUnCompteurSiPsionique(),
        Soigner_Interdit(),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.AlterEgoAction, action).SetCostFunc(CostFunc.Exhaust("YouControlUnit")),
    ]
