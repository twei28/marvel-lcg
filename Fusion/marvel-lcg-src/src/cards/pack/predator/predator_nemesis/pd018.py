from . import *

# * Xenomorph Drone — SBIRE (set « Predator Nemesis »). XENOMORPH. PV 3, MNG 1, ATQ 2, Boost ★ + 1. Guard. Teamwork (XENOMORPH).
# Forced Response: After Xenomorph Drone engages you, if there are no other minions engaged with you, deal yourself 1
#   facedown encounter card.
# ★ Boost: Put Xenomorph Drone into play engaged with you.
#
# Cartes de reference :
#  - `38029` Donald Pierce : `AfterMinionEngagePlayer(ForcedResponse, "This", "You", op)` ;
#  - `01121` Weapons Runner : `WhenCardBecomeBoost("This", PutThisIntoPlay)` (helper de `cards/pack/__init__.py`) ;
#  - `ar012` / `16118` Badoon Grunt : `player.DealEncounterCards(1, effect)` pour « deal yourself 1 facedown encounter card » ;
#  - `Guard` et `Teamwork` : bases automatiques (`desc`, fiches guard.md, teamwork.md), AUCUN script.
#
# ⚠ Mots-pieges :
#  - « If there are NO OTHER minions engaged with you » : les AUTRES sbires engages avec CE joueur (le Drone ne compte pas).
#  - « After Drone engages YOU » : « you » = le joueur auquel il vient de s'engager.
#  - « ★ Boost » : icone etoile du cadre de boost (`desc.Boost "1**"` = 1 icone + l'etoile) ; une carte de boost entre en jeu
#    engagee avec le joueur vise.


def GetAbilities() -> Sequence['Ability']:

    def essaim(effect: 'Effect', message: 'Message.AfterMinionEngagePlayer') -> None:
        this = effect.this.CastTo(Minion)
        joueur = message.GetToPlayer()
        if joueur is None:
            return
        autres = [m for m in joueur.GetEngagedMinions() if m is not this]
        if not autres:
            joueur.DealEncounterCards(1, effect)

    return [
        AbilityFactory.AfterMinionEngagePlayer(
            AbilityType.ForcedResponse,
            "This",
            "You",
            essaim,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            PutThisIntoPlay,
        ),
    ]
