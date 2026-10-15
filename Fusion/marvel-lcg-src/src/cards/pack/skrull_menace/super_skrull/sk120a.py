from . import *
from cards.pack.skrull_menace.campaign import CampaignSetup

# Searching for the Heir 1A — complot principal, face A (mise en place).
# Contents: Super-Skrull I and Super-Skrull II (Super-Skrull III for expert
#   mode). Super-Skrull and Standard encounter sets. Two modular encounter sets
#   (Army of Skrulls and Kree-Skrull War).
# Setup: Shuffle each SUPERPOWER attachment into the SUPERPOWER deck and set it
#   next to the encounter deck.
#
# Cartes de reference :
#  - **`hs107a`** (Kraven, 1A) + `hunting_season/trap` : `WhenCardSetup("This")`
#    cree le paquet de scenario nomme et y melange les cartes mises de cote
#    (`CreerPaquetSuperpouvoir`, helper du set). Un 1A sans TargetThreat avance
#    seul en 1B (scheme_main.py) : ne PAS appeler Advance (lecon gb004a).
#  - **`skrull_empire/sk082a`** : meme squelette (Setup d'un complot 1A custom).
#
# ⚠ Choix :
#  - « Contents » : decrit par data/scenarios/sk_super_skrull(_expert).json
#    (mechants I+II, ou II+III en expert ; Standard (+ Expert) ; Army of Skrulls
#    et Kree-Skrull War).
#  - Le Super-Skrull est deja en jeu (etape 9 de la mise en place) quand ce Setup
#    part (etape 12) : le paquet est lie a lui, comme les pieges de Kraven.
#  - Les 4 attachements arrivent dans le json en `set_aside` (sk122-sk125).


def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        Unused(message)
        CreerPaquetSuperpouvoir(effect)

    return [
        *CampaignSetup(2),  # mode campagne : mise en place, regle de cooperation, releve du carnet
        AbilityFactory.WhenCardSetup("This", mise_en_place),
    ]
