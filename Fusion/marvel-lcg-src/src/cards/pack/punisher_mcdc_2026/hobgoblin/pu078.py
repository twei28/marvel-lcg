from . import *

# Torn to Pieces — OBLIGATION (pas d'icone de boost).
# Forced Response : After your hero uses a basic power, resolve the "Pumpkin Bomb" ability.
# Alter-Ego Action : Exhaust your identity and discard 3 cards from the encounter deck → discard this card.
#
# Cartes de reference : ares/ares/ar010.py (obligation : `PlayerActionToDiscardThis(AlterEgoAction)` +
# `CostFunc.Exhaust("YourIdentity")`), galactic_storm gs065 (`AfterUnitUseBasicPower`).
#
# ⚠ « your HERO uses a basic power » : ATQ, THW ou DEF du heros lui-meme (`powers="Hero"`), pas ses allies ; « resolve
# the Pumpkin Bomb » : une fois par pouvoir utilise ; l'action ne se joue qu'en alter ego (cout : epuiser l'identite,
# puis defausser 3 cartes de rencontre, puis la defausse).

def GetAbilities() -> Sequence['Ability']:

    def apres_pouvoir(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        joueur = message.trigger.GetControlByPlayer() or Worlds.GetFirstPlayer(effect)
        ResoudrePumpkinBomb(effect, joueur, 1)

    def trois_cartes(effect: 'Effect', message: 'Message2') -> None:
        Worlds.DiscardEncounterCards(3, effect)

    return [
        AbilityFactory.AfterUnitUseBasicPower(AbilityType.ForcedResponse, "You", apres_pouvoir, powers="Hero"),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.AlterEgoAction,
            ex_operation=trois_cartes,
        ).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
    ]
