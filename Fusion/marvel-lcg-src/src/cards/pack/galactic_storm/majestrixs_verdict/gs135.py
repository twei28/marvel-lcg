from . import *

# Birthright to the Throne — TRAITRISE (Majestrix's Verdict), 2 exemplaires. 1 icone de boost.
# When Revealed: If the Shi'ar Throne support is in play, Deathbird attacks the player who controls it (even if
#   that player is in alter ego form). Otherwise, Deathbird schemes.
# [star] Boost: Give Deathbird a tough status card.
#
# Cartes de reference :
#  - « X attacks the player who controls <carte> (even if that player is in alter-ego form) » :
#    `villain.DoAttackYou(joueur, effect)`, modele OFFICIEL 16114 Single-Minded Fury (« Ronan attacks the player
#    who controls the Power Stone (even if ... alter-ego form) »).
#  - « Otherwise, Deathbird schemes » : `DoSchemes(joueur, effect)` (modele 50096 Leaping Kick).
#  - Boost : `Faces.GiveStatus([deathbird], "Tough")` (modele sk151, 52037).
#
# ⚠ Mots-pieges : « the player WHO CONTROLS IT » (pas forcement celui qui revele) ; « the Shi'ar Throne
# SUPPORT » (la face manigance ne compte pas) ; « Otherwise, Deathbird schemes » contre le joueur qui revele ;
# l'Interruption forcee de Deathbird peut detourner cette attaque vers un STARJAMMER de ce joueur.


def GetAbilities() -> Sequence['Ability']:

    def droit_de_naissance(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        deathbird = DeathbirdEnJeu(effect)
        if deathbird is None:
            return
        trone = TroneSoutienEnJeu(effect)
        controleur = trone.GetControlBy() if trone is not None else None
        if controleur is not None and controleur.IsPlayer():
            deathbird.DoAttackYou(controleur, effect)
        else:
            deathbird.DoSchemes(message.GetToPlayer(), effect)

    def robuste(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Unused(message)
        deathbird = DeathbirdEnJeu(effect)
        if deathbird is not None:
            Faces.GiveStatus([deathbird], "Tough", effect)

    return [
        AbilityFactory.WhenThisRevealed(None, droit_de_naissance),
        AbilityFactory.WhenCardBecomeBoost("This", robuste),
    ]
