from . import *

# * Iron Lad (face alter-ego, Nathaniel Richards)
# Inventive Genius — Action: Reduce the resource cost of the next TECH card
#   played this phase by 2. (Limit once per round.)
#
# Modele : Evaluate Threat (hercules/59028.py),
# `Worlds.UpdateNextCardPlayCost(player, -2, effect, finder=CardFinder(...),
# in_this='Phase')`, ici filtre sur `trait="TECH"` au lieu d'une carte precise.
#
# Porte aussi la regle speciale de l'insert (reshuffle -> revele aussi Kang
# the Conqueror) : voir SetupReshuffleNemesis dans __init__.py.

def GetAbilities() -> Sequence['Ability']:

    def inventive_genius(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)

        initiator = effect.GetInitiator()
        Worlds.UpdateNextCardPlayCost(initiator, -2, effect, finder=CardFinder(trait="TECH"), in_this='Phase')

    return [
        SetupReshuffleNemesis(),

        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            inventive_genius
        ).SetName("Inventive Genius")
        .LimitOncePerRound(),
    ]
