from . import *

# * Faith — SBIRE (ELITE. SLAYER. HELLMOUTH). SCH 2, ATQ 2*, PV 6, boost 2. Patrol. Villainous. Victory 0.
# [star] Faith's attacks gain overkill.
# When Defeated: Find the set-aside Faith ally and put her into play under any player's control.
#
# CARTES DE REFERENCE
#  - `07091`-like / `UnitAttackGainKeyword("This", overkill=True)` (27078) ; `32159` pour le « When Defeated » ; `Patrol`, `Villainous`, `Victory` : `desc`.
#
# TEXTE CONTRE CODE
#  « the set-aside Faith ALLY » -> filtre `Ally` (le sbire porte le meme nom), zone de mise de cote seule (liee a ce sbire par `desc.Linked`).
#  « under ANY player's control » -> `ChoisirUnJoueur` (seul : le joueur ; a plusieurs : il choisit).


def GetAbilities() -> Sequence['Ability']:

    def faith(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        joueur = message.GetKillerPlayer() or Worlds.GetFirstPlayer(effect)
        alliee = Search.SearchForCard(effect, joueur, include_set_aside=True, name=NOM_FAITH, card_type=Ally)
        if alliee:
            alliee.PutIntoPlay(ChoisirUnJoueur(effect, joueur), effect, under_control=True)

    return [
        AbilityFactory.UnitAttackGainKeyword(
            "This",
            overkill=True,
        ),
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            faith,
        ),
    ]
