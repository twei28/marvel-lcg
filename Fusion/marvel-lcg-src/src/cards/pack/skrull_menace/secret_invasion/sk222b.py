from . import *

# * Korya — SBIRE (paquet IMPOSTOR, face B). IMPOSTOR. REVEALED. SKRULL. 3 PV, SCH 1, ATQ 2.
# When Revealed: Heal all damage from Korya and put her into play engaged with you.
# [star] <b>Forced Response</b>: After Korya attacks you, discard the top card of each player's deck.
#
# Cartes de reference :
#  - « When Revealed: Heal all damage from X and put it into play engaged with you » : **`gambit 37034`** Psionic Shield
#    (`HealthUnits([unite], "All", effect)`) et **`sk098`** (le sbire engage le joueur qui revele) ; helper `SbireImpostor()`.
# ★ Forced Response « After X attacks you, discard the top card of each player's deck » : `AfterUnitAttackYou(ForcedResponse,
# "This", ...)` (**`sk150`**, **`32073`** Avalanche) + `Players.ForEachPlayer` / `DiscardDeckTopCards` (**`gb022`**, `mojo`).
#
# ⚠ Mots-pieges : « heal ALL damage » (un allie retourne arrive blesse) ; « engaged with YOU » : le joueur qui revele
# (pour un allie retourne : celui qui le controlait avant, livret p. 16) ; la face sbire quitte le jeu vers la DEFAUSSE
# IMPOSTOR (livret p. 16, liaison `BindDiscardPile`).


def GetAbilities() -> Sequence['Ability']:
    def defausser(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        Unused(message)
        Players.ForEachPlayer(effect, lambda joueur: joueur.DiscardDeckTopCards(1, effect))

    return [
        *SbireImpostor(),
        AbilityFactory.AfterUnitAttackYou(AbilityType.ForcedResponse, "This", defausser),
    ]
