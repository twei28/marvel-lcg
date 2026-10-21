from . import *

# Gang War (1A) — MANIGANCE PRINCIPALE, mise en place.
# Contents : 3 CAPO villains, side A (B for expert). The Big Apple, 9 location & 9 LEAD cards, and Standard sets. Two modular sets.
#   (Optional : Uptown Expansion.)                                (portee par data/scenarios/big_apple*.json)
# Setup : Place the 9 locations in numerical order in a 3x3 grid. Place one chosen CAPO villain next to each row. Create the 9-card LEADS
#   deck. Reveal The City and Never Sleeps environments. Each player reveals a card from the LEADS deck.
#
# Cartes de reference : galactic_storm/earth_under_siege/gs161a.py (`WhenCardSetup("This")`, `villain: []` dans le scenario,
# `Villains.BuildVillainDeck/RevealNextVillain/SetRule`), briques `Ville.Installer` et zone commune (spec M1/M2), paquet LEADS (`CreerPaquetPistes`).
# ⚠ « Place the 9 locations in NUMERICAL order » : pu030..pu038 en 3 rangees de 3 ; chaque lieu est dans la zone de SA rangee ; The City,
# Never Sleeps et le complot principal dans la zone COMMUNE ; tous les joueurs partent a Midtown.

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        MettreEnPlaceLaVille(effect)

    return [AbilityFactory.WhenCardSetup("This", mise_en_place)]
