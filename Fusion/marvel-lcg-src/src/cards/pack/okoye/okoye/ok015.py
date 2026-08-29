from . import *

# Vibranium Spear (1/2) — TECH. WEAPON. Restricted.
# Attach to a friendly WAKANDA character. Restricted. Max 1 per character.
# Attached character gets +1 ATK (+2 ATK instead if attached to an ally) and
#   its basic attacks gain piercing.
#
# Exemplaire physique 1 de 2 (ok015, ok016). Bonus ATK CONDITIONNEL selon le
# type de porteur : `AbilityFactory.GiveKeywordToAttached(..., attack=1,
# get_new_value=...)`. `get_new_value(effect, face, faces)` renvoie le
# multiplicateur applique a `attack=1` (asset_helper.py:201-208,
# `face.Gain(effect, diff, attack=attack, ...)`) : 2 sur un Ally, 1 sinon --
# donne exactement +1 ou +2 ATK.
#
# "its basic attacks gain piercing" : `AbilityFactory.UnitAttackGainKeyword`,
# modele albert/albert/ab008.py (meme carte : +ATK en jeu + piercing sur
# attaque de base), mais avec un attaquant DYNAMIQUE (le porteur peut etre
# n'importe quel WAKANDA, pas un nom fixe) via `CardFinder(check_effect_fn=
# ...)` qui lit `effect.this.attached_face` (can_attach.py:106-110, la face
# actuellement attachee a CETTE carte).


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
