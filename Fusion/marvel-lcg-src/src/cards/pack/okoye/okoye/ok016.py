from . import *

# Vibranium Spear (2/2)
# Exemplaire physique 2 de 2, contenu identique a ok015 (voir ce fichier pour
# le detail du modele repris).


CIBLE = CardFinder(card_type=Friend, trait="WAKANDA")


def _valeur_atk(effect: 'Effect', face: 'CardFace', faces: List['CardFace']) -> int:
    Unused(effect, faces)
    return 2 if Ally.IsType(face) else 1


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisUpgradeCard(CIBLE),
        *AbilityFactory.GiveKeywordToAttached(
            CIBLE,
            attack=1,
            get_new_value=_valeur_atk,
        ),
        AbilityFactory.UnitAttackGainKeyword(
            CardFinder(check_effect_fn=lambda effect, face: effect.this.attached_face == face),
            is_basic_attack=True,
            piercing=True,
        ),
    ]
