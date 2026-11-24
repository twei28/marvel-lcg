from . import *

# Friends of Ours — TRAITRISE. Boost 1.
# When Revealed : Find a MAGGIA minion that is not in play and reveal it. Each MAGGIA minion activates against the
#   player it is engaged with.
#
# Cartes de reference : `Find.FindAndReveal` (agent_13/ag001b, jigsaw/pu065) et la brique
# `Worlds.Enemies.AllMinionActivateAgainstEngagedPlayer(effect, trait=...)` (game/operate/enemies.py).
#
# ⚠ Ordre : d'abord on TROUVE ET REVELE (le nouveau sbire s'engage et entre dans le lot), ensuite TOUS les MAGGIA
# engages s'activent, y compris celui qu'on vient de reveler. « activates » = attaque ou manigance selon la phase
# (un sbire s'active contre le joueur engage avec lui, brique commune).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        Find.FindAndReveal(effect, joueur, trait="MAGGIA", card_type=Minion)
        Worlds.Enemies.AllMinionActivateAgainstEngagedPlayer(effect, trait="MAGGIA")

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
