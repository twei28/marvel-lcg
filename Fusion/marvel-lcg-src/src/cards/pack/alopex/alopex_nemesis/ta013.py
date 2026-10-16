from . import *

# You Belong To Me — COMPLOT ANNEXE nemesis (1/5). Hazard 1, StartingThreat 2*,
# Boost 2.
# Kitsune has dug her claws into Alopex, and she has no intention of letting
#   her go...
# When Revealed: Each player discards 1 card from their hand.
#
# Cartes de reference :
#  - `WhenThisRevealed(None, op)` sur un complot annexe : `an011`, `ho014`,
#    `leonardo/tl014` ;
#  - « each player discards 1 card from their hand » :
#    `Players.ForEachPlayer(effect, fn)` (`raphael/tr014`) + le helper du set
#    `DefausserUneCarteDeLaMain` (modele `57062`).
#
# ⚠ BASES AUTOMATIQUES (desc, aucun script) : `StartingThreat 2*` (« 2 » +
# silhouette = PAR JOUEUR), `Boost 2` (deux icones « Y »), `Hazard 1` (icone
# « carte penchee + croix evidee », SANS barre dessous : verifiee par
# comparaison au glyphe `H` de ChampionsIcons.ttf, fiche hazard.md).
#
# Mots-pieges :
#  - « EACH PLAYER » : chaque joueur, pas seulement celui qui a revele ;
#  - « discards 1 card FROM THEIR HAND » : le joueur CHOISIT ; main vide = rien ;
#  - pas de limite imprimee.


def GetAbilities() -> Sequence['Ability']:

    def you_belong_to_me(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this, message)

        def chacun(joueur: 'Player') -> None:
            DefausserUneCarteDeLaMain(joueur, effect)

        Players.ForEachPlayer(effect, chacun)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            you_belong_to_me,
        ),
    ]
