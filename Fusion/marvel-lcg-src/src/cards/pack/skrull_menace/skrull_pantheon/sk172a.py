from . import *

# * Kly'bn (III) — MECHANT, stade 3 (une face de la carte double face sk172a/sk172b). SCH 3, ATQ 2, 20 PV par joueur. GOD. SKRULL.
# When Revealed: Place 1 faith counter on Kly'bn and give him a tough status card.
# Forced Response: After resolving step one of the villain phase, discard the top card of the encounter deck for each faith counter on Kly'bn. Deal the players each non-treachery card discarded this way as a facedown encounter card in player order.
#
# Cartes de reference :
#  - Reponse apres l'etape 1 de la phase du mechant : `hunting_season/hs226` Master Trapper
#    (`AbilityFactory.AfterResolveVillainPhaseStep(ForcedResponse, 1, op)`) ; defausse du dessus du
#    deck rencontre : `Worlds.DiscardEncounterCards(n, effect)` (modele sk106 / sk139, rend les
#    cartes defaussees) ; distribution face cachee : `player.DealEncounterCard(face, effect)`
#    (modele 27087b / 53031).
#  - Carte double face : `fne/typhoid_mary/60110a` (vilain recto-verso, `"villain": ["a,b"]`) ;
#    jeton : `Faces.PlaceCountersOn([this], 1, 'faith', effect)` (compteur maison, card_face.py) ;
#    statut : `Faces.GiveStatus([this], "Tough", effect)` (modele sk151 Metallic Skin).
#
# ⚠ Mots-pieges : « for each FAITH counter ON Kly'bn » (le compteur de CETTE carte, partage par les
# deux faces) ; « non-treachery card » (les traitrises restent defaussees, les autres sont distribuees) ; « in player order » (une carte a la fois, du premier joueur
# au dernier, puis on recommence) ; « AFTER resolving step one » (Reponse apres l'etape 1, avant les
# activations) ; « give him a tough status card (stade III : la carte d'etat Robuste est redonnee a CHAQUE revelation, donc a chaque retournement) ».


def GetAbilities() -> Sequence['Ability']:
    return [
        RevelationDuMechant(True),
        ReponseFoi(False),
    ]
