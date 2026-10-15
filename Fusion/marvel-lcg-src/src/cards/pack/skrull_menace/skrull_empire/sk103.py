from . import *

# Giving Orders — TRAITRISE x2 (Skrull Empire). 1 boost.
# When Revealed: Each SKRULL minion activates against the player it is engaged
#   with. If no minion activated this way, this card gains surge.
#
# Carte de reference : **`36039`** Astral Attack ;
# `Worlds.Enemies.AllMinionActivateAgainstEngagedPlayer(effect, trait=...,
# if_no_activate=...)` (operate/enemies.py) + `ThisCardGainSurge`.
# ⚠ « EACH SKRULL minion », chacun contre SON joueur ; « activates » (attaque
# en heros, manigance en civil, regle native).


def GetAbilities() -> Sequence['Ability']:

    def ordres(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        Worlds.Enemies.AllMinionActivateAgainstEngagedPlayer(
            effect, trait="SKRULL", if_no_activate=lambda: ThisCardGainSurge(effect))

    return [AbilityFactory.WhenThisRevealed(None, ordres)]
