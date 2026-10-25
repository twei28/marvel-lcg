from . import *

# Bide Time — MANIGANCE ANNEXE (x2). Menace de depart 2, Crisis 1, Boost 3.
# When Defeated: The player who defeated this scheme resolves the "Special" ability on the copy of Bleeding Out attached to their identity.
#
# Cartes de reference :
#  - « When Defeated » d'une manigance annexe : `WhenSchemeBeDefeated(WhenDefeated, "This", op)` + `message.defeating_player`
#    (`br012`, `gs120a`) ; `Crisis` : `desc.Crisis` natif (fiche mots-cles/crisis.md).
#
# ⚠ Mots-pieges :
#  - icone du coin = CRISIS (glyphe `C` de ChampionsIcons.ttf, comparee a Crowd Control 01108) : tant qu'elle est en jeu, on ne peut pas
#    retirer de menace du complot principal ;
#  - « the player who DEFEATED » : celui qui a retire la derniere menace, PAS le joueur a qui elle a ete revelee ;
#  - menace de depart fixe (2, aucune icone par joueur) ; trois icones Boost.


def GetAbilities() -> Sequence['Ability']:

    def vaincue(effect: 'Effect', message: 'Message.WhenSchemeWouldBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)

        ResoudreSaignement(effect, message.defeating_player)

    return [
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            vaincue,
        ),
    ]
