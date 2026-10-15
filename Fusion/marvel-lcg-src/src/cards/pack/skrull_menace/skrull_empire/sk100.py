from . import *

# Emperor's Throne — COMPLOT ANNEXE (Skrull Empire). Menace 2[per_hero],
# Acceleration + Hazard, 3 boosts.
# When Defeated: The villain attacks the player who defeated this scheme (even
#   if that player is in alter-ego form). Give the villain 1 additional boost
#   card for this activation.
#
# Cartes de reference : **`32072`** Feral Rage : `WhenSchemeBeDefeated(
# WhenDefeated, "This", op, has_defeating_player=True)` +
# `villain.DoAttackYou(message.GetDefeatingPlayer(), effect)` ; **`60093`**
# pour « 1 additional boost card for this activation »
# (`WhenUnitWouldAttack.GiveAdditionalBoostCardForThisActivation`), passe ici
# par le crochet `operation=` de DoAttackYou (attaque de CETTE carte seulement).
# ⚠ « the villain » : le mechant COURANT ; « even if ... alter-ego » : aucun
# filtre de forme. Icones : desc (Acceleration/Hazard verifiees le 15/10).


def GetAbilities() -> Sequence['Ability']:

    def trone(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        joueur = message.GetDefeatingPlayer()
        mechant = Worlds.FindVillain(effect)
        if joueur is None or mechant is None:
            return
        mechant.DoAttackYou(
            joueur, effect,
            operation=lambda attaque: attaque.GiveAdditionalBoostCardForThisActivation(1, effect),
        )

    return [
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", trone, has_defeating_player=True),
    ]
