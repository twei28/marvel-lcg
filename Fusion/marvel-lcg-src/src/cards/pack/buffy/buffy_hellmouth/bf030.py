from . import *

# * The Master — SBIRE (ELITE. VAMPIRE. HELLMOUTH). SCH 2, ATQ 2, PV 3[per_hero], Toughness, Victory 0.
# When Defeated: Find Angelus and put him into play engaged with your identity.
#
# CARTES DE REFERENCE
#  - `32159` Fabian Cortez : `WhenUnitBeDefeated(WhenDefeated, "This", op)` + `message.GetKillerPlayer()` + `minion.PutIntoPlay(player, effect)`.
#  - `Toughness`, `Victory` : natifs dans `desc` (fiches `mots-cles/toughness.md`, `victory.md`).
#
# TEXTE CONTRE CODE
#  « engaged with YOUR identity » -> le joueur qui a vaincu (un sbire mis en jeu par `PutIntoPlay(joueur, ..)` s'engage avec lui).


def GetAbilities() -> Sequence['Ability']:

    def the_master(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        joueur = message.GetKillerPlayer() or Worlds.GetFirstPlayer(effect)
        angelus = Trouver(effect, joueur, NOM_ANGELUS, Minion)
        if angelus:
            angelus.PutIntoPlay(joueur, effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            the_master,
        ),
    ]
