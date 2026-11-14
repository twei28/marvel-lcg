from . import *

# Stalking Prey — MANIGANCE ANNEXE. Menace de depart 3, Hazard 1, Boost 2.
# When Revealed: Place additional threat here equal to the number of bleed counters on the copy of Bleeding Out attached to your
#   identity.
#
# Cartes de reference :
#  - menace posee a la revelation : `this.PlaceThreatOnSchemes([this], n, effect)` (`01107`) ; compteurs : `face.GetCounters('bleed')`.
#
# ⚠ Mots-pieges :
#  - icone du coin = HAZARD (glyphe `H`, comparee a Breakin' & Takin' 01107) : une carte de rencontre de plus ;
#  - « ADDITIONAL » : s'ajoute aux 3 menaces de depart ; « YOUR identity » : le joueur a qui la carte est revelee ;
#  - sans copie de Bleeding Out (cas theorique) : +0 ;
#  - homonyme `hs123`/`hs124` (Kraven) : ne jamais chercher par nom.


def GetAbilities() -> Sequence['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)

        saignement = LeSaignement(message.GetToPlayer())
        n = saignement.GetCounters('bleed') if saignement is not None else 0
        if n > 0:
            this.PlaceThreatOnSchemes([this], n, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelee,
        ),
    ]
