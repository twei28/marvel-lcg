from . import *

# * Grrix — SBIRE (paquet IMPOSTOR, face B). IMPOSTOR. REVEALED. SKRULL. 3 PV, SCH 2, ATQ 1.
# When Revealed: Heal all damage from Grrix and put him into play engaged with you.
# <b>When Defeated</b>: The villain attacks the player who defeated Grrix <i>(even if that player is in alter-ego form)</i>.
#
# Cartes de reference :
#  - « When Revealed: Heal all damage from X and put it into play engaged with you » : **`gambit 37034`** Psionic Shield
#    (`HealthUnits([unite], "All", effect)`) et **`sk098`** (le sbire engage le joueur qui revele) ; helper `SbireImpostor()`.
# « The villain attacks the player who defeated X (even if that player is in alter-ego form) » : **`sk100`** Emperor's Throne
# (MEME phrase pour un complot annexe : `villain.DoAttackYou(joueur, effect)`, aucun filtre de forme).
#
# ⚠ Mots-pieges : « heal ALL damage » (un allie retourne arrive blesse) ; « engaged with YOU » : le joueur qui revele
# (pour un allie retourne : celui qui le controlait avant, livret p. 16) ; la face sbire quitte le jeu vers la DEFAUSSE
# IMPOSTOR (livret p. 16, liaison `BindDiscardPile`).


def GetAbilities() -> Sequence['Ability']:
    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        Unused(message)
        joueur = message.GetKillerPlayer()
        mechant = Worlds.FindVillain(effect)
        if joueur is not None and mechant is not None:
            mechant.DoAttackYou(joueur, effect)

    return [
        *SbireImpostor(),
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
    ]
