from . import *

# * Vermin — SBIRE (New Revengers). REVENGER. PV 5, MNG 1, ATQ 2 (etoile), boost 1 + etoile.
# [star] Vermin's attacks deal indirect damage.
# [star] Boost: If this activation is an attack, it deals indirect damage.
#
# Cartes de reference :
#  - « attacks deal indirect damage » : **`iceman 46025`** * Pyro (`UnitAttackGainKeyword("This",
#    indirect_damage=True)`).
#  - Boost conditionnel a l'attaque : **`sm 27122`** Symbiotic Monstrosity (`WhenCardBecomeBoost("This", fn,
#    during_attack=True)` + `message.would_atk_message.SetDealIndirectDamage(effect)`).
#
# ⚠ Mots-pieges : « ATTACKS » (toutes ses attaques, pas seulement de base) ; « IF this activation IS AN
# ATTACK » : le Boost n'agit pas sur une manigance (`during_attack=True`) ; ce Boost vaut pour l'activation
# du mechant/sbire qui retourne la carte, la ou le texte permanent ne vaut que pour Vermin lui-meme.


def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        attaque = getattr(message, 'would_atk_message', None)
        if attaque is not None:
            attaque.SetDealIndirectDamage(effect)

    return [
        AbilityFactory.UnitAttackGainKeyword("This", indirect_damage=True),
        AbilityFactory.WhenCardBecomeBoost("This", boost, during_attack=True),
    ]
