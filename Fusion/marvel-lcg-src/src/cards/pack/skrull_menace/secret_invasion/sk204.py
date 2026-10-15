from . import *

# Glory to the Skrull Empire — TRAITRISE x2 (Secret Invasion). ★ + 2 boosts.
# When Revealed: Give the villain and each SKRULL minion engaged with you a tough status card. If the villain already has a
#   tough status card, this card gains surge.
# ★ Boost: Give the villain a tough status card.
#
# Cartes de reference : **`Faces.GiveStatus(units, "Tough", effect)`** (faces.py) ; surge : **`sk103`** (`ThisCardGainSurge`) ;
# `Worlds.FindVillain`.
#
# ⚠ Mots-pieges : « If the villain ALREADY has a tough status card » : testee AVANT de donner les statuts ; « each SKRULL minion
# engaged WITH YOU » (pas les sbires des autres joueurs) ; un personnage ne porte qu'UNE carte Robuste (le moteur refuse la
# seconde) ; Boost : le mechant seulement.


def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        mechant = Veranke(effect)
        deja = mechant is not None and mechant.IsTough()
        cibles = [m for m in joueur.GetEngagedMinions() if m.HasTrait("SKRULL")]
        if mechant is not None:
            cibles.insert(0, mechant)
        Faces.GiveStatus(cibles, "Tough", effect)
        if deja:
            ThisCardGainSurge(effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Unused(message)
        mechant = Veranke(effect)
        if mechant is not None:
            Faces.GiveStatus([mechant], "Tough", effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelation),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
