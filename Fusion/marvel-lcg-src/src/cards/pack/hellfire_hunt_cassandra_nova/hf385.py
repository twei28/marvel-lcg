from . import *

# Wild Sentinel (SBIRE SENTINEL, x4 : hf382-hf385). PV 4, ATK 2, SCH 1, Boost 3. « When Defeated : The defeating player chooses to either take 2 damage
# or place this card on the bottom of the encounter deck instead of the discard pile. »
# Cartes de reference : sl033-sl034 (`WhenUnitBeDefeated(WhenDefeated, "This")`, `defeating_player`), 39015b (`WhenCardWouldDiscard` +
# `SetBeInstead` + `Card.MoveToBottom` : « instead of the discard pile »), mt011 (`ChooseAbilities` a deux options).
# ⚠ « instead of the discard pile » : la carte n'atteint JAMAIS la defausse : le choix pose un drapeau, que l'Interruption forcee de defausse lit ;
# sans joueur vainqueur (defaite par un effet), rien n'est propose et la carte va a la defausse.


def GetAbilities() -> Sequence['Ability']:
    return SentinelleSauvage()
