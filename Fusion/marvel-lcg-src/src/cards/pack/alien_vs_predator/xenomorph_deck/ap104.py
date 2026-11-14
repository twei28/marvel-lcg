from . import *

# Alien Scout (13-16, 4 exemplaires) — SBIRE. XENOMORPH. SCH 1, ATK 2, PV 2. Deck Xenomorph (dos rouge).
# Teamwork ([[XENOMORPH]]).
# Forced Interrupt: When you would draw or discard this card from your deck, draw 1 card. Deal this card to yourself as a facedown encounter card.
# When Defeated: Place Alien Scout in your discard pile.
#
# Cartes de reference :
#  - Teamwork (XENOMORPH) : `desc.Teamwork`, natif (fiche teamwork.md).
#  - Interruption depuis le deck du joueur : 27087b Maze of Mirrors (pioche ET defausse du deck, `SetBeInstead`, `DealEncounterCard`) ;
#    carte de rencontre vivant dans un deck joueur : fiche weakness.md ;
#  - « Place in your discard pile » : deplacement apres la defaite (`AfterUnitBeDefeated`) vers la defausse du joueur engage.
#
# ⚠ Mots-pieges :
#  - « draw OR DISCARD this card FROM YOUR DECK » : une defausse depuis la MAIN n'est pas concernee ;
#  - « your discard pile » : celle du JOUEUR (pas la defausse de rencontre) ; elle revient donc dans son deck au remelange ;
#  - donnee comme boost par Expanding Hive ? Non : 2 PV imprimes (< 3).


def GetAbilities() -> Sequence['Ability']:
    return CapacitesScout(True)
