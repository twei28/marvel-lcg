from . import *

# Facehugger — ATTACHEMENT. CONDITION. XENOMORPH. Boost 1. Deux exemplaires (16, 17).
# Attach to your identity.
# Forced Response: After your turn ends, take 2 damage and place 2 threat on the main scheme.
# Alter-Ego Action: Search the encounter deck and discard pile for a [[XENOMORPH]] minion and reveal it → discard this card.
#
# Cartes de reference : 21029 Sap Power (comme ap013) ; « search the encounter deck and discard pile ... reveal it » :
#   `Search.EncounterCard(.., include_discard_pile=True)` + `Reveal` (helper `ChercherEtReveler`).
#
# ⚠ Mots-pieges :
#  - recherche limitee au deck ET a la defausse de RENCONTRE (pas « Find ») : les Alien Scout des decks joueurs n'y sont pas ;
#  - trouver est le cout : sans sbire XENOMORPH a cet endroit, l'action n'est pas proposee.


def EnRencontre(effect: 'Effect') -> bool:
    tas = list(Worlds.GetEncounterDeckCards(effect)) + list(Worlds.GetEncounterDiscardPileCards(effect))
    return any(Minion.IsType(f) and f.HasTrait("XENOMORPH") for f in tas)


def GetAbilities() -> Sequence['Ability']:
    return CibleMarquee("XENOMORPH",
                        lambda effect, joueur: ChercherEtReveler(effect, joueur, "XENOMORPH"),
                        EnRencontre)
