from . import *

# The Infiltration Has Begun 1A — complot principal, face A (mise en place).
# Contents: Spider-Woman I and Spider-Woman II (Spider-Woman II and Spider-Woman III instead for expert mode). Secret
#   Invasion and Standard encounter sets. One modular encounter set (Army of Skrulls).
# Setup: Create the IMPOSTOR deck and set it next to the encounter deck (see insert). Put the "Who Do You Trust?"
#   environment into play.
#
# Cartes de reference :
#  - **`skrull_empire/sk082a`** (Setup d'un 1A custom : `WhenCardSetup("This", ...)`, environnement mis de cote puis
#    `PutIntoPlay`) et **`super_skrull/sk120a`** (creation d'un paquet de scenario nomme a la mise en place) ;
#    **`hs107a`** (Kraven, 1A) + `hunting_season/trap` pour le paquet nomme.
#
# ⚠ Mots-pieges :
#  - « Contents » : decrit par data/scenarios/sk_secret_invasion(_expert).json (mechants I+II, ou II+III en expert ;
#    Secret Invasion + Standard (+ Expert) ; Army of Skrulls).
#  - « Create the IMPOSTOR deck » : les 20 cartes double face mises de cote, melangees (`CreerPaquetImpostor`).
#  - « Put the environment into play » : MISE EN JEU (pas une revelation) ; l'environnement est mis de cote par le json.
#  - Veranke est deja en jeu (etape 9 de la mise en place) quand ce Setup part : le paquet est lie a elle.
#  - Un 1A sans TargetThreat avance seul en 1B (scheme_main.py) : ne PAS appeler Advance (lecon gb004a).


def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        Unused(message)
        CreerPaquetImpostor(effect)
        env = [f for f in Worlds.AsideDeck(effect).Get(True) if f.paper.card_id == ID_ENVIRONNEMENT]
        if env:
            env[0].PutIntoPlay(Worlds.GetFirstPlayer(effect), effect)

    return [
        AbilityFactory.WhenCardSetup("This", mise_en_place),
    ]
