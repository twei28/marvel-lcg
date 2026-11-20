from . import *

# * Lord Deathstrike — SBIRE. HAND. Patrol. SCH 2 / ATQ 2 / PV 5, boost ★ seul.
# When Revealed : If Shifting Corridors is in play, shuffle the top 2 cards of the encounter deck into the trap deck ; otherwise, reveal the top card of the trap deck.
# ★ Boost : Put this minion into play engaged with you.
#
# Cartes de reference : spot/31036 (`WhenCardBecomeBoost("This", PutThisIntoPlay)` : « put this minion into play engaged with you »), `MelangerDansPaquetPiege` /
# `ReveleDuPaquetPiege` (ce module : precedent hunting_season/trap, skrull_empire `RevelerPlanete`), patrol.md (Patrol natif).
# ⚠ Mots-pieges : « the TOP 2 cards of the encounter deck » : les deux du dessus, melangees DANS le paquet piege (elles quittent le deck de rencontre) ; « otherwise,
#  REVEAL the top card of the trap deck » : revelee au joueur qui revele Lord Deathstrike ; en Boost la carte n'est PAS revelee (elle entre en jeu, engagee : pas de When
#  Revealed) ; Patrol : natif (desc).


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        if Corridors(effect) is not None:
            MelangerDansPaquetPiege(effect, du_deck_rencontre=2)
        else:
            ReveleDuPaquetPiege(effect, joueur)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", PutThisIntoPlay),
    ]
