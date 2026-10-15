from . import *

# Arrival of Impostors — TRAITRISE (Secret Invasion). ★ + 2 boosts.
# When Revealed: Each player puts a CAMOUFLAGED ally at random from the IMPOSTOR deck into play under their control.
# ★ Boost: Put a CAMOUFLAGED ally at random from the IMPOSTOR deck into play under your control.
#
# Cartes de reference : **`fne 60113b`** (`Players.ForEachPlayer(effect, action)`, une action par joueur) ; boost :
# **`sk104`** Long Live the Empire (`WhenCardBecomeBoost("This", boost)`, `message.GetToPlayer()`). Mise en jeu : helper
# `MettreAllieCamoufle` (le dessus du paquet melange = « at random »).
#
# ⚠ Mots-pieges : « EACH player » : un allie par joueur, dans l'ordre des joueurs, chacun sous SON controle (la limite d'allies
# s'applique : un allie en trop se defausse, donc se RETOURNE) ; « at random » : carte du dessus du paquet melange ; « under
# YOUR control » (Boost) : le joueur a qui la carte est retournee.


def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        Players.ForEachPlayer(effect, lambda joueur: MettreAllieCamoufle(effect, joueur))

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        MettreAllieCamoufle(effect, message.GetToPlayer())

    return [
        AbilityFactory.WhenThisRevealed(None, revelation),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
