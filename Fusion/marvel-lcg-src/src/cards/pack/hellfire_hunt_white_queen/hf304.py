from . import *

# Illusory Defender. Attachement ILLUSION PSIONIC. « Attach to your identity. Uses (1 illusion counter). Attacks against you cannot be defended by
# allies or other identities. When Revealed : ... Forced Response : After the villain attacks you, remove 1 illusion counter from here. »
# Cartes de reference : sk201 / 27152 (`UnitCannotDefend`), 55039 (`AfterUnitAttackYou`).
# ⚠ LIMITE (QUESTIONS.md n°3) : le message `CheckIfUnitCanDefendAgainstAttack` ne dit pas QUI est attaque ; en SOLO « attacks against you » et
# « toutes les attaques » sont la meme chose. A plusieurs joueurs, la restriction vaut pour toute attaque ou le defenseur est un allie / une
# autre identite que le porteur.


def GetAbilities() -> Sequence['Ability']:
    def apres_attaque_du_vilain(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        RetirerUnCompteurIllusion(effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay("YourIdentity"),
        PoserUnCompteurSiPsionique(),
        *AbilityFactory.UnitCannotDefend(CardFinder(card_type=Ally | Hero), Enemy, cannot_trigger_defense_ability=False),
        AbilityFactory.AfterUnitAttackYou(AbilityType.ForcedResponse, Villain, apres_attaque_du_vilain),
    ]
