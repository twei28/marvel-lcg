from . import *

# Infiltration Ritual — TRAITRISE x2 (Secret Invasion). ★.
# When Revealed: Put a CAMOUFLAGED ally at random from the IMPOSTOR deck into play under any player's control. If you cannot,
#   this card gains surge.
# ★ Boost: Remove 3 suspicion counters from "Who Do You Trust?".
#
# Cartes de reference : helpers `ChoisirJoueur` / `MettreAllieCamoufle` (set) ; surge : **`sk103`** (`ThisCardGainSurge`) ;
# Boost : **`sk104`** (`WhenCardBecomeBoost`), `RetirerSoupcons`.
#
# ⚠ Mots-pieges : « under ANY player's control » : le joueur qui revele DESIGNE le joueur (lui-meme compris) ; « If you cannot » :
# paquet et defausse IMPOSTOR vides (aucun allie a mettre en jeu) ; Boost : 3 jetons (« Remove 3 »), pas par joueur.


def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = ChoisirJoueur(effect, message.GetToPlayer())
        if MettreAllieCamoufle(effect, joueur) is None:
            ThisCardGainSurge(effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Unused(message)
        RetirerSoupcons(effect, 3)

    return [
        AbilityFactory.WhenThisRevealed(None, revelation),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
