from . import *

# * SP//dr Suit
#
# ERRATA RRG 1.7 / 1.8 (Annexe V, SP//dr #1B) : « Return to Base — Forced Interrupt: When you flip to this side, flip SP//dr to Peni Parker. Detach Peni Parker from here,
#   moving all counters on THIS card and cards attached to THIS card to HER. » (ANCIEN texte : l'inverse, « moving all counters on her and cards attached to her to this card »).
#   `Spdr()` (`__init__.py`) deplace jetons, compteurs, ameliorations, statuts et PV de l'identite SORTANTE vers l'identite ENTRANTE dans les deux sens : au retour (armure -> Peni)
#   c'est donc deja le sens du NOUVEAU texte. A VALIDER par les cas `31001b` de `tools/cas/errata_rrg.py` (aller-retour avec compteurs et amelioration).

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.ThisCannotBeTreatedAsBlank(),
        Spdr().SetName("Return to Base"),
        Spdr2(),
    ]

